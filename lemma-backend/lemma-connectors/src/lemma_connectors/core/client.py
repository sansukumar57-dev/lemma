from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping

from lemma_connectors.core.auth import CredentialTypes
from lemma_connectors.core.descriptors import OperationDescriptor, ToolDescriptor
from lemma_connectors.core.errors import OperationNotFoundError, ToolNotFoundError
from lemma_connectors.core.openapi import (
    GeneratedTool,
    build_generated_client,
    build_tool_map,
)
from lemma_connectors.core.operations import Operation


class BaseInfoClient:
    def __init__(
        self,
        *,
        metadata_path: Path,
        base_url: str,
        client_module_path: str,
    ):
        self._generated_client = build_generated_client(
            client_module_path=client_module_path,
            base_url=base_url,
            credentials=None,
        )
        self._tools = build_tool_map(
            metadata_path=metadata_path,
            generated_client=self._generated_client,
        )
        self._operations: dict[str, Operation[Any, Any]] = {}
        self.resources = SimpleNamespace()

    def list_tools(self) -> list[ToolDescriptor]:
        return [tool.descriptor for tool in self._tools.values()]

    def get_tool(self, name: str) -> GeneratedTool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise ToolNotFoundError(name) from exc

    def list_operations(self) -> list[OperationDescriptor]:
        return [operation.descriptor for operation in self._operations.values()]

    def get_operation(self, name: str) -> Operation[Any, Any]:
        try:
            return self._operations[name]
        except KeyError as exc:
            raise OperationNotFoundError(name) from exc

    def register_resources(self, resources: dict[str, Any]) -> None:
        self.resources = SimpleNamespace(**resources)
        operations: dict[str, Operation[Any, Any]] = {}
        for resource in resources.values():
            operations.update(resource.build_operations())
        self._operations = operations


class BaseIntegrationClient(BaseInfoClient):
    def __init__(
        self,
        *,
        metadata_path: Path,
        base_url: str,
        client_module_path: str,
        credentials: CredentialTypes | None,
    ):
        self.credentials = credentials
        self._generated_client = build_generated_client(
            client_module_path=client_module_path,
            base_url=base_url,
            credentials=credentials,
        )
        self._tools = build_tool_map(
            metadata_path=metadata_path,
            generated_client=self._generated_client,
        )
        self._operations: dict[str, Operation[Any, Any]] = {}
        self.resources = SimpleNamespace()

    async def execute_tool(self, name: str, payload: Mapping[str, Any] | None = None) -> Any:
        tool = self.get_tool(name)
        return await tool.execute(payload)

    async def execute_operation(
        self,
        name: str,
        payload: Mapping[str, Any] | Any,
    ) -> Any:
        operation = self.get_operation(name)
        return await operation.execute(payload)
