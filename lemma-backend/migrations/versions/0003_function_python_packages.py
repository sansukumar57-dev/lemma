"""Function python_packages.

Adds ``functions.python_packages`` — a JSONB list of pip requirement specifiers
declared in the function code's ``#python_packages:`` header. The agentbox
function executor installs these before running the function. The server-side
default backfills existing rows to ``[]``.

Revision ID: 0003_function_python_packages
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0003_function_python_packages"
down_revision = "0002_org_join_policy"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "functions",
        sa.Column(
            "python_packages",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )


def downgrade() -> None:
    op.drop_column("functions", "python_packages")
