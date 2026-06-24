from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ConnectorHelperAgentRequest(BaseModel):
    """Request model for the connector helper agent."""

    app_names: list[str] = Field(
        description="Connector IDs the agent may use while planning the goal."
    )
    goal: str = Field(
        description="What the caller wants to achieve with one or more connectors."
    )


class ConnectorHelperAgentResponse(BaseModel):
    """Response model for the connector helper agent."""

    success: bool = Field(
        description="Whether the helper agent completed successfully."
    )
    answer_markdown: Optional[str] = Field(
        default=None,
        description="Detailed markdown guidance for accomplishing the requested goal.",
    )
    operations_by_app: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Recommended operation names grouped by connector.",
    )
    message: Optional[str] = Field(
        default=None,
        description="Human-readable status message.",
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message when the helper agent fails.",
    )


class ConnectorHelperAgentOutput(BaseModel):
    """Structured output produced by the connector helper agent."""

    answer_markdown: str = Field(
        description=(
            "Detailed markdown explanation of how to achieve the goal, including "
            "which operations to inspect first and what to watch out for."
        )
    )
    operations_by_app: dict[str, list[str]] = Field(
        description="Recommended operation names grouped by connector."
    )
