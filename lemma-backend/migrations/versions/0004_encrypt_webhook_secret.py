"""Widen agent_surfaces.webhook_secret for encryption at rest.

The webhook secret is now encrypted via ``app/core/crypto`` (a compact
``lsenc1:`` envelope longer than the raw secret), so the column must hold more
than the previous ``String(255)``. Widen it to ``Text``. Existing plaintext rows
keep working (the cipher reads unprefixed values as plaintext) and are encrypted
on next save or by ``scripts/reencrypt_secrets.py``.

Revision ID: 0004_encrypt_webhook_secret
"""

from alembic import op
import sqlalchemy as sa

revision = "0004_encrypt_webhook_secret"
down_revision = "0003_function_python_packages"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "agent_surfaces",
        "webhook_secret",
        existing_type=sa.String(length=255),
        type_=sa.Text(),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "agent_surfaces",
        "webhook_secret",
        existing_type=sa.Text(),
        type_=sa.String(length=255),
        existing_nullable=True,
    )
