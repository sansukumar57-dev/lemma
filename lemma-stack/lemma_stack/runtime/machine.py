"""Podman machine (macOS/Windows VM) and Linux socket management."""

from __future__ import annotations

import json
import platform
import subprocess

from lemma_stack.output import AdminError, info

MACHINE_NAME = "lemma-runtime"
MACHINE_MEMORY_MB = 6144
MACHINE_CPUS = 4
MACHINE_DISK_GB = 100


def _run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(args, capture_output=True, text=True, check=False)
    if check and proc.returncode != 0:
        raise AdminError(f"{' '.join(args)} failed: {(proc.stderr or '').strip()}")
    return proc


def _machines() -> list[dict]:
    proc = _run(["podman", "machine", "list", "--format", "json"], check=False)
    if proc.returncode != 0 or not proc.stdout.strip():
        return []
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []


def ensure_podman_ready(runtime) -> None:
    system = platform.system()
    if system == "Linux":
        _ensure_linux_socket()
        return
    _ensure_machine()


def _ensure_machine() -> None:
    machines = _machines()
    existing = next((m for m in machines if m.get("Name") == MACHINE_NAME), None)
    default = next((m for m in machines if m.get("Default")), None)

    # Respect any already-running machine (e.g. the user's default) instead of
    # spinning up a second VM.
    for m in machines:
        if m.get("Running"):
            return

    if existing is None and default is None:
        info(
            f"Creating podman machine '{MACHINE_NAME}' "
            f"({MACHINE_MEMORY_MB} MiB RAM, {MACHINE_CPUS} CPUs, {MACHINE_DISK_GB} GiB disk)…"
        )
        _run(
            [
                "podman",
                "machine",
                "init",
                MACHINE_NAME,
                "--memory",
                str(MACHINE_MEMORY_MB),
                "--cpus",
                str(MACHINE_CPUS),
                "--disk-size",
                str(MACHINE_DISK_GB),
                "--rootful=false",
                "--now",
            ]
        )
        return

    target = MACHINE_NAME if existing is not None else str(default.get("Name"))
    info(f"Starting podman machine '{target}'…")
    _run(["podman", "machine", "start", target])


def _ensure_linux_socket() -> None:
    # Rootless podman needs the user API socket for the agentbox manager.
    proc = _run(
        ["systemctl", "--user", "enable", "--now", "podman.socket"],
        check=False,
    )
    if proc.returncode != 0:
        info("note: could not enable podman.socket via systemd; relying on existing socket")
