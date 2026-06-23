"""Function adapter for the workflow module."""

from functools import partial
from pathlib import Path
from typing import Any, Dict
from uuid import UUID

from app.core.authorization.context import Context
from app.core.config import settings
from app.core.infrastructure.db.uow import SqlAlchemyUnitOfWork
from app.core.infrastructure.jobs.streaq_job_queue import get_streaq_job_queue
from app.modules.workflow.domain.ports import FunctionPort
from app.modules.function.domain.entities import FunctionType


class FunctionControlAdapter(FunctionPort):
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.uow = uow

        # Initialize dependencies for FunctionService
        from app.modules.workspace.services.workspace_sandbox_service import (
            WorkspaceSandboxService,
        )
        from app.modules.function.services.function_file_manager import (
            FunctionFileManager,
        )
        from app.modules.function.services.function_service import FunctionService
        from app.modules.function.infrastructure.repositories import (
            FunctionRepository,
            FunctionRunRepository,
        )
        from app.core.infrastructure.events.message_bus import get_message_bus
        from app.modules.pod.services.authorization_factory import (
            create_authorization_service,
        )

        self.workspace_service = WorkspaceSandboxService()
        self.run_repository = FunctionRunRepository(uow)
        message_bus = get_message_bus()
        if settings.effective_storage_backend() == "gcs":
            if not settings.gcs_storage_bucket:
                raise ValueError("GCS storage requires GCS_STORAGE_BUCKET")
            function_storage_factory = partial(
                FunctionFileManager,
                bucket_name=settings.gcs_storage_bucket,
            )
        else:
            function_storage_factory = partial(
                FunctionFileManager,
                root_path=Path(settings.local_file_storage_root) / "common",
            )

        self.function_service = FunctionService(
            function_repository=FunctionRepository(uow, message_bus=message_bus),
            run_repository=FunctionRunRepository(uow, message_bus=message_bus),
            workspace_service=self.workspace_service,
            storage_factory=function_storage_factory,
            job_queue=get_streaq_job_queue(),
            authorization_service=create_authorization_service(uow),
        )

    async def execute_function(
        self,
        function_name: str,
        inputs: Dict[str, Any],
        pod_id: UUID,
        user_id: UUID,
        ctx: Context | None = None,
    ) -> Any:
        run = await self.function_service.execute_function(
            pod_id=pod_id,
            name=function_name,
            input_data=inputs,
            user_id=user_id,
            ctx=ctx,
        )

        if run.status == "COMPLETED":  # FunctionRunStatus.COMPLETED
            return run.output_data
        elif run.status == "FAILED":
            raise RuntimeError(f"Function execution failed: {run.error}")

        function = await self.function_service.repository.get(run.function_id)
        if function is not None and function.type == FunctionType.JOB:
            return {
                "run_id": str(run.id),
                "status": run.status,
                "function_type": FunctionType.JOB.value,
            }

        raise RuntimeError(
            "API function execution returned a non-terminal run; API functions "
            "must complete inline"
        )

    async def get_run_status(self, function_run_id: UUID) -> Dict[str, Any]:
        """Status/output of a function run, for completion reconciliation."""
        run = await self.run_repository.get_run(function_run_id)
        if run is None:
            return {"status": "NOT_FOUND"}
        status = str(run.status.value if hasattr(run.status, "value") else run.status)
        if status == "COMPLETED":
            return {"status": "COMPLETED", "output_data": run.output_data or {}}
        if status == "FAILED":
            return {
                "status": "FAILED",
                "error": run.error or "Function run failed",
                "output_data": run.output_data or {},
            }
        return {"status": "RUNNING"}
