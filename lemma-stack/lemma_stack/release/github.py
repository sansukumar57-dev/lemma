"""GitHub auth for private repos: manifest fetch via the API + ghcr login.

Public repos need none of this — the plain release-asset URL works. While the
repo is private, the manifest asset must be downloaded through the GitHub API
with a token, and image pulls need a ghcr.io login. Tokens are discovered
from GITHUB_TOKEN / GH_TOKEN, falling back to the system `gh` CLI.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.request
from typing import Any

from lemma_stack.output import AdminError, info, warn


def github_token() -> str | None:
    for var in ("GITHUB_TOKEN", "GH_TOKEN"):
        token = os.environ.get(var)
        if token:
            return token
    if shutil.which("gh"):
        proc = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=False
        )
        token = proc.stdout.strip()
        if proc.returncode == 0 and token:
            return token
    return None


def _api_get(url: str, token: str, *, accept: str = "application/vnd.github+json") -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": accept,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def fetch_manifest_via_api(repo: str, channel: str, asset_name: str, token: str) -> dict[str, Any]:
    """Resolve a release (latest or v<version>) and download its manifest asset."""
    if channel == "stable":
        release_url = f"https://api.github.com/repos/{repo}/releases/latest"
    else:
        tag = f"v{channel.lstrip('v')}"
        release_url = f"https://api.github.com/repos/{repo}/releases/tags/{tag}"
    try:
        release = json.loads(_api_get(release_url, token).decode("utf-8"))
    except OSError as exc:
        raise AdminError(f"could not fetch release info from {release_url}: {exc}") from exc

    asset = next(
        (a for a in release.get("assets", []) if a.get("name") == asset_name),
        None,
    )
    if asset is None:
        raise AdminError(
            f"release {release.get('tag_name')} has no {asset_name} asset; "
            "was it published by the release-local-images workflow?"
        )
    try:
        payload = _api_get(str(asset["url"]), token, accept="application/octet-stream")
    except OSError as exc:
        raise AdminError(f"could not download {asset_name}: {exc}") from exc
    return json.loads(payload.decode("utf-8"))


def _github_username(token: str) -> str:
    if shutil.which("gh"):
        proc = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True,
            text=True,
            check=False,
        )
        login = proc.stdout.strip()
        if proc.returncode == 0 and login:
            return login
    try:
        data = json.loads(_api_get("https://api.github.com/user", token).decode("utf-8"))
        if data.get("login"):
            return str(data["login"])
    except OSError:
        pass
    return "x-access-token"


def login_ghcr(runtime, token: str) -> bool:
    """Log the container runtime into ghcr.io; best-effort (pull errors surface later)."""
    username = _github_username(token)
    proc = subprocess.run(
        [runtime.cli, "login", "ghcr.io", "-u", username, "--password-stdin"],
        input=token,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        warn(f"ghcr.io login failed: {(proc.stderr or '').strip()}")
        return False
    info(f"logged in to ghcr.io as {username}")
    return True
