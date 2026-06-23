"""Uppercase internal enum values for consistency.

Standardizes the values of internal-domain enums to UPPERCASE to match the rest
of the codebase (state/kind/type enums are CAPS). Only the genuinely-internal,
persisted enums are migrated here:

  * ``agent_messages.kind`` (MessageKind: text -> TEXT, tool_call -> TOOL_CALL, …)
  * ``usage_records.usage_kind`` (UsageKind: llm -> LLM, …)
  * ``agent_surface_conversation_links.last_event->>'conversation_type'``
    (surfaces ConversationType: external_dm -> EXTERNAL_DM, …)

NOT migrated (intentionally left lowercase — external/wire contracts):
  * ``agent_messages.role`` (MessageRole) — LLM-ecosystem convention.
  * REST query operators, vendor/provider identifiers, MIME types.

Idempotent: re-running ``UPPER``/``LOWER`` on already-converted rows is a no-op.

Revision ID: 0005_uppercase_internal_enums
"""

from alembic import op

revision = "0005_uppercase_internal_enums"
down_revision = "0004_encrypt_webhook_secret"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # MessageKind — agent_messages.kind (leave agent_messages.role lowercase).
    op.execute("UPDATE agent_messages SET kind = UPPER(kind)")

    # UsageKind — usage_records.usage_kind.
    op.execute("UPDATE usage_records SET usage_kind = UPPER(usage_kind)")

    # surfaces ConversationType — embedded in the last_event JSONB blob.
    op.execute(
        """
        UPDATE agent_surface_conversation_links
        SET last_event = jsonb_set(
            last_event,
            '{conversation_type}',
            to_jsonb(UPPER(last_event ->> 'conversation_type'))
        )
        WHERE last_event ? 'conversation_type'
        """
    )


def downgrade() -> None:
    op.execute("UPDATE agent_messages SET kind = LOWER(kind)")
    op.execute("UPDATE usage_records SET usage_kind = LOWER(usage_kind)")
    op.execute(
        """
        UPDATE agent_surface_conversation_links
        SET last_event = jsonb_set(
            last_event,
            '{conversation_type}',
            to_jsonb(LOWER(last_event ->> 'conversation_type'))
        )
        WHERE last_event ? 'conversation_type'
        """
    )
