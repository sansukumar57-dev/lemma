from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any


class StreamTextState:
    """Buffers incremental text snapshots and emits token/message events."""

    def __init__(
        self,
        *,
        harness_kind: str,
        event_sink: Callable[[str, Any], Awaitable[None]] | None,
    ) -> None:
        self.harness_kind = harness_kind
        self.event_sink = event_sink
        self.current_text = ""
        self.flushed_texts: list[str] = []
        self.streamed_tokens = False
        self.streamed_messages = False
        self.emitted_tool_call_ids: set[str] = set()

    @property
    def full_text(self) -> str:
        parts = [*self.flushed_texts]
        if self.current_text.strip():
            parts.append(self.current_text.strip())
        return "\n".join(parts)

    async def update_text_snapshot(self, text: str) -> None:
        if not text:
            return
        if text == self.current_text:
            return
        if self.current_text and not text.startswith(self.current_text):
            await self.flush(is_final=False)
        delta = text[len(self.current_text):] if text.startswith(self.current_text) else text
        self.current_text = text
        if self.event_sink is not None and delta:
            self.streamed_tokens = True
            await self.event_sink("token", {"kind": "text", "data": delta})

    async def flush(self, *, is_final: bool) -> None:
        text = self.current_text.strip()
        self.current_text = ""
        if not text:
            return
        self.flushed_texts.append(text)
        if self.event_sink is None:
            return
        self.streamed_messages = True
        await emit_assistant_text_message(
            self.event_sink,
            text,
            harness_kind=self.harness_kind,
            is_final=is_final,
        )


async def emit_assistant_text_message(
    event_sink: Callable[[str, Any], Awaitable[None]],
    text: str,
    *,
    harness_kind: str,
    is_final: bool,
) -> None:
    metadata: dict[str, object] = {
        "user_daemon": True,
        "harness_kind": harness_kind,
    }
    if not is_final:
        metadata["is_final_answer"] = False
    await event_sink(
        "message",
        {
            "role": "assistant",
            "kind": "text",
            "text": text,
            "metadata": metadata,
        },
    )
