"""Tests for the agent_surfaces pod-deletion cleanup handler."""

from __future__ import annotations

import logging
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.modules.agent_surfaces.events import handlers


@pytest.mark.asyncio
async def test_on_pod_deleted_removes_pod_surfaces(monkeypatch):
    service = AsyncMock()
    service.delete_all_surfaces_for_pod.return_value = 2
    monkeypatch.setattr(handlers, "get_surface_service", lambda uow: service)

    pod_id = uuid4()
    event = {
        "event_type": "pod.deleted",
        "pod_id": str(pod_id),
        "organization_id": str(uuid4()),
    }

    await handlers.on_pod_deleted(event, logging.getLogger("test"), uow=AsyncMock())

    service.delete_all_surfaces_for_pod.assert_awaited_once_with(pod_id)


@pytest.mark.asyncio
async def test_on_pod_deleted_ignores_non_delete_events(monkeypatch):
    service = AsyncMock()
    monkeypatch.setattr(handlers, "get_surface_service", lambda uow: service)

    event = {
        "event_type": "pod.member.removed",
        "pod_id": str(uuid4()),
        "user_id": str(uuid4()),
    }

    await handlers.on_pod_deleted(event, logging.getLogger("test"), uow=AsyncMock())

    service.delete_all_surfaces_for_pod.assert_not_awaited()
