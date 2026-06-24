from __future__ import annotations

import os

import pytest

# AgentBox config is required to construct workspace/function services. Default
# to test-only values (set before app.core.config is imported) so suites run
# without a configured local AgentBox manager; workspace-marked e2e tests
# override these with a real local manager via their fixtures.
os.environ.setdefault("AGENTBOX_API_KEY", "test-agentbox-key")
os.environ.setdefault("AGENTBOX_API_URL", "http://localhost:9999")

WORKSPACE_FIXTURES = {
    "backend_server",
    "configure_workspace_api_url",
    "workspace_image",
    "_configure_function_workspace_api_url",
}

AGENT_PROVIDER_TESTS = {
    "test_file_creation_tool_call_streams_tool_json_tokens",
    "test_stopping_streaming_agent_run_does_not_wedge_worker",
    "test_task_conversation_waits_then_completes_with_real_worker_model",
    "test_pod_agent_http_lifecycle_with_real_worker_model",
    "test_pod_assistant_http_lifecycle_with_real_worker_model",
    "test_first_run_generates_title_with_real_worker_model",
    "test_agent_tool_http_apis",
}


def pytest_collection_modifyitems(config, items):
    """Classify e2e tests by the expensive runtime fixtures they request."""

    run_provider_e2e = os.getenv("LEMMA_RUN_PROVIDER_E2E") == "1"
    provider_skip = pytest.mark.skip(
        reason="Set LEMMA_RUN_PROVIDER_E2E=1 to run real provider-backed e2e tests."
    )

    for item in items:
        path_parts = set(item.path.parts)
        if {"tests", "e2e"}.issubset(path_parts):
            item.add_marker(pytest.mark.e2e)
        fixture_names = set(getattr(item, "fixturenames", ()))
        if "worker" in fixture_names:
            item.add_marker(pytest.mark.worker)
        if fixture_names & WORKSPACE_FIXTURES:
            item.add_marker(pytest.mark.workspace)
        if (
            (
                item.path.name == "test_agent_usage_e2e.py"
                and item.originalname
                == "test_agent_run_records_usage_and_usage_apis_filter_it"
            )
            or (
                item.path.name == "test_agent_e2e.py"
                and item.originalname in AGENT_PROVIDER_TESTS
            )
        ):
            item.add_marker(pytest.mark.provider)

        marker_names = {marker.name for marker in item.iter_markers()}
        if "provider" in marker_names and not run_provider_e2e:
            item.add_marker(provider_skip)


def pytest_sessionstart(session: pytest.Session) -> None:
    del session
    from app.modules.test_support import e2e_base

    e2e_base._cleanup_e2e_workspace_containers()


def pytest_runtest_teardown(item: pytest.Item, nextitem: pytest.Item | None) -> None:
    del nextitem
    if "workspace" not in {marker.name for marker in item.iter_markers()}:
        return
    from app.modules.test_support import e2e_base

    e2e_base._cleanup_e2e_workspace_containers()


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    del session, exitstatus
    from app.modules.test_support import e2e_base

    e2e_base._cleanup_e2e_workspace_containers()
    e2e_base._close_shared_contexts()
