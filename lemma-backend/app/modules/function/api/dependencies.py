"""Function module dependencies."""

from functools import partial
from pathlib import Path
from typing import Annotated
from fastapi import Depends

from app.core.api.dependencies import UoWDep
from app.core.authorization.context import ResourceType
from app.core.authorization.dependencies import (
    pod_from_path,
    require_action,
    require_resource_admin_or_creator,
    require_resource_action,
)
from app.core.authorization.permissions import Permissions
from app.core.infrastructure.events.message_bus import get_message_bus
from app.core.infrastructure.jobs.streaq_job_queue import get_streaq_job_queue
from app.modules.icon.services.icon_service import IconService
from app.modules.workspace.services.workspace_tool_runtime import (
    get_function_workspace_runtime,
)
from app.modules.function.infrastructure.repositories import (
    FunctionRepository,
    FunctionRunRepository,
)
from app.modules.function.services.function_file_manager import FunctionFileManager
from app.modules.function.services.function_service import FunctionService
from app.modules.pod.services.authorization_factory import create_authorization_service
from app.core.config import settings


def _get_function_storage_factory():
    if settings.effective_storage_backend() == "gcs":
        if not settings.gcs_storage_bucket:
            raise ValueError("GCS storage requires GCS_STORAGE_BUCKET")
        return partial(FunctionFileManager, bucket_name=settings.gcs_storage_bucket)
    return partial(
        FunctionFileManager,
        root_path=Path(settings.local_file_storage_root) / "common",
    )


def get_function_service(uow: UoWDep) -> FunctionService:
    """Provide FunctionService."""
    message_bus = get_message_bus()
    workspace_service = get_function_workspace_runtime()
    return FunctionService(
        function_repository=FunctionRepository(uow, message_bus=message_bus),
        run_repository=FunctionRunRepository(uow, message_bus=message_bus),
        workspace_service=workspace_service,
        storage_factory=_get_function_storage_factory(),
        job_queue=get_streaq_job_queue(),
        icon_service=IconService(),
        authorization_service=create_authorization_service(uow),
    )


FunctionServiceDep = Annotated[FunctionService, Depends(get_function_service)]

# Auth dependencies for controller routes
FunctionViewerDep = require_action(Permissions.FUNCTION_READ, pod_from_path)
FunctionEditorDep = require_action(Permissions.FUNCTION_UPDATE, pod_from_path)
FunctionAdminDep = require_action(Permissions.FUNCTION_DELETE, pod_from_path)
FunctionExecuteDep = require_action(Permissions.FUNCTION_EXECUTE, pod_from_path)
FunctionResourceViewerDep = require_resource_action(
    Permissions.FUNCTION_READ,
    resource_type=ResourceType.FUNCTION,
    name_param="function_name",
)
FunctionResourceEditorDep = require_resource_action(
    Permissions.FUNCTION_UPDATE,
    resource_type=ResourceType.FUNCTION,
    name_param="function_name",
)
FunctionResourceAdminDep = require_resource_action(
    Permissions.FUNCTION_DELETE,
    resource_type=ResourceType.FUNCTION,
    name_param="function_name",
)
FunctionResourceDeleteDep = require_resource_admin_or_creator(
    Permissions.FUNCTION_DELETE,
    resource_type=ResourceType.FUNCTION,
    name_param="function_name",
)
FunctionResourceExecuteDep = require_resource_action(
    Permissions.FUNCTION_EXECUTE,
    resource_type=ResourceType.FUNCTION,
    name_param="function_name",
)
