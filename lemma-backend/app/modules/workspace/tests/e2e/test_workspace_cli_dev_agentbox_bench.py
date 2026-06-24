"""Run the real backend tool path against agentbox-DEV with lemma -> ngrok backend.

Unlike the local-agentbox bench, this points settings.agentbox_api_url at
api-dev.agentbox.work and injects the real Lemma env (fresh signin token from the
ngrok backend + real org/pod), using the real user so the sandbox lands on dev.
This reproduces what the agent actually experiences and isolates whether the
"3-4 parallel tool calls get stuck/fail" symptom comes from our backend layer or
from the remote sandbox.

Run:
    PYTHONPATH=. uv run pytest -s -p no:cacheprovider \
      app/modules/workspace/tests/e2e/test_workspace_cli_dev_agentbox_bench.py
"""
from __future__ import annotations

import asyncio
import contextlib
import time
from uuid import UUID, uuid4

import httpx
import pytest

from app.core.config import settings
from app.modules.agent.tools.context import BaseAgentContext
from app.modules.agent.tools.workspace_cli import workspace_cli
from app.modules.agent.tools.workspace_cli.models import ExecCommandRequest
from app.modules.workspace.services import (
    workspace_sandbox_service as wss_mod,
    workspace_env_cache as envc_mod,
)
from app.modules.workspace.services.workspace_tool_runtime import (
    reset_workspace_tool_runtimes,
)

pytestmark = [pytest.mark.e2e, pytest.mark.workspace]

DEV_AGENTBOX_URL = "https://api-dev.agentbox.work"
DEV_AGENTBOX_KEY = "replace-with-a-long-random-token"
NGROK = "https://dc9c-2406-7400-54-39e6-00-100c.ngrok-free.app"
USER_ID = "d0f7be8a-67a5-40c9-bca8-c90589a5ffa3"
ORG_ID = "019e90f2-efb4-72c8-85a4-e9978537251c"
POD_ID = "019ea060-3203-722e-853e-d933051925b0"


def _signin_token() -> str:
    r = httpx.post(
        f"{NGROK}/st/auth/signin",
        headers={"Content-Type": "application/json", "rid": "emailpassword"},
        json={"formFields": [
            {"id": "email", "value": "anukul@gappy.ai"},
            {"id": "password", "value": "@nukulG@ppy786"},
        ]},
        timeout=30,
    )
    r.raise_for_status()
    return r.headers["st-access-token"]


@pytest.fixture
def dev_agentbox_env(e2e_settings):
    real_env = {
        "LEMMA_TOKEN": _signin_token(),
        "LEMMA_BASE_URL": NGROK,
        "LEMMA_AUTH_URL": NGROK + "/auth",
        "LEMMA_ORG_ID": ORG_ID,
        "LEMMA_POD_ID": POD_ID,
    }
    orig = (settings.agentbox_api_url, settings.agentbox_api_key, settings.api_url)
    settings.agentbox_api_url = DEV_AGENTBOX_URL
    settings.agentbox_api_key = DEV_AGENTBOX_KEY
    settings.api_url = NGROK
    reset_workspace_tool_runtimes()

    orig_get_env = wss_mod.WorkspaceSandboxService.get_env_vars
    orig_cache_get = envc_mod.RedisWorkspaceEnvCache.get

    async def fake_get_env_vars(self, *a, **k):  # noqa: ANN001
        return dict(real_env)

    async def fake_cache_get(self, key):  # noqa: ANN001
        return None  # force miss so the injected env is always used

    wss_mod.WorkspaceSandboxService.get_env_vars = fake_get_env_vars
    envc_mod.RedisWorkspaceEnvCache.get = fake_cache_get
    try:
        yield real_env
    finally:
        wss_mod.WorkspaceSandboxService.get_env_vars = orig_get_env
        envc_mod.RedisWorkspaceEnvCache.get = orig_cache_get
        (settings.agentbox_api_url, settings.agentbox_api_key, settings.api_url) = orig
        reset_workspace_tool_runtimes()


async def _run(ctx, cmd, *, timeout=120):
    started = time.perf_counter()
    res = await workspace_cli.exec_command_internal(
        ctx, ExecCommandRequest(cmd=cmd, timeout_seconds=timeout)
    )
    return time.perf_counter() - started, res


def _fmt(xs):
    return "[" + ", ".join(f"{x:.2f}" for x in xs) + "]"


async def test_dev_agentbox_parallel_tool_calls(dev_agentbox_env):
    del dev_agentbox_env
    ctx = BaseAgentContext(
        user_id=UUID(USER_ID),
        org_id=UUID(ORG_ID),
        pod_id=UUID(POD_ID),
        conversation_id=uuid4(),
        agent_name="dev-bench",
        workload_type="agent",
    )

    print("\n========== DEV AGENTBOX TOOL-PATH BENCH ==========")
    try:
        # cold start
        dt0, r0 = await _run(ctx, "echo warm")
        print(f"cold start (first exec):        {dt0:6.2f}s  ok={r0.success}  err={r0.error}")

        # backend overhead probe (no lemma): single + parallel sleep 1
        dt, r = await _run(ctx, "sleep 1")
        print(f"single 'sleep 1':               {dt:6.2f}s  (backend overhead {dt-1:.2f}s) ok={r.success}")

        for n in (3, 4):
            t0 = time.perf_counter()
            res = await asyncio.gather(*[_run(ctx, "sleep 1") for _ in range(n)], return_exceptions=True)
            wall = time.perf_counter() - t0
            lat = [c[0] for c in res if isinstance(c, tuple)]
            ok = sum(1 for c in res if isinstance(c, tuple) and c[1].success)
            factor = wall / max(lat) if lat else 0
            print(f"parallel x{n} 'sleep 1':          wall={wall:6.2f}s {_fmt(lat)} ok={ok}/{n} serialization={factor:.2f}x")
            for c in res:
                if isinstance(c, tuple) and not c[1].success:
                    print(f"    FAIL: {c[1].error}")
                elif not isinstance(c, tuple):
                    print(f"    EXC: {repr(c)[:140]}")

        # REAL workload: lemma pods list, sequential then parallel
        dt, r = await _run(ctx, "lemma --json pods list")
        print(f"single 'lemma pods list':       {dt:6.2f}s ok={r.success}  err={r.error}")

        for n in (3, 4):
            t0 = time.perf_counter()
            res = await asyncio.gather(*[_run(ctx, "lemma --json pods list") for _ in range(n)], return_exceptions=True)
            wall = time.perf_counter() - t0
            lat = [c[0] for c in res if isinstance(c, tuple)]
            ok = sum(1 for c in res if isinstance(c, tuple) and c[1].success)
            print(f"parallel x{n} 'lemma pods list':  wall={wall:6.2f}s {_fmt(lat)} ok={ok}/{n}")
            for c in res:
                if isinstance(c, tuple) and not c[1].success:
                    print(f"    FAIL: {c[1].error}")
                elif not isinstance(c, tuple):
                    print(f"    EXC: {repr(c)[:140]}")
        print("==================================================\n")
    finally:
        with contextlib.suppress(Exception):
            await wss_mod.WorkspaceSandboxService().stop_sandbox(UUID(USER_ID))
