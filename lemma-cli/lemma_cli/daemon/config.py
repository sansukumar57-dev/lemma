from __future__ import annotations

import json
import os
import platform
import socket
from pathlib import Path
from uuid import uuid4

DAEMON_DIR = Path("~/.lemma/daemon").expanduser()
DAEMON_CONFIG_PATH = DAEMON_DIR / "config.json"
DAEMON_PID_PATH = DAEMON_DIR / "daemon.pid"
DAEMON_LOG_PATH = DAEMON_DIR / "logs" / "daemon.log"


def ensure_config() -> dict:
    DAEMON_DIR.mkdir(parents=True, exist_ok=True)
    config = load_config()
    if not config.get("device_key"):
        config["device_key"] = str(uuid4())
    if not config.get("display_name"):
        config["display_name"] = socket.gethostname()
    save_config(config)
    return config


def load_config() -> dict:
    if not DAEMON_CONFIG_PATH.exists():
        return {}
    try:
        data = json.loads(DAEMON_CONFIG_PATH.read_text())
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def save_config(config: dict) -> None:
    DAEMON_CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")


def device_info() -> dict[str, str]:
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system().lower(),
        "platform_version": platform.version(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    }


def daemon_ws_url(base_url: str) -> str:
    root = base_url.rstrip("/")
    if root.startswith("https://"):
        root = "wss://" + root.removeprefix("https://")
    elif root.startswith("http://"):
        root = "ws://" + root.removeprefix("http://")
    else:
        # No recognized scheme (e.g. a bare host) — assume TLS, like a browser.
        root = "wss://" + root.removeprefix("//")
    return f"{root}/me/agent-runtime/daemon/ws"


def read_pid() -> int | None:
    if not DAEMON_PID_PATH.exists():
        return None
    try:
        return int(DAEMON_PID_PATH.read_text().strip())
    except ValueError:
        return None


def process_is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True
