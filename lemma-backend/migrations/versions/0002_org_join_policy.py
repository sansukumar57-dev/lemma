"""Organization join_policy.

Replaces ``organizations.allow_auto_join`` (bool) with an ordered
``join_policy`` enum-string (INVITE_ONLY / EMAIL_DOMAIN / PUBLIC) and frees
``email_domain`` values that were held by orgs not using the EMAIL_DOMAIN
policy, so the global unique index only constrains domain-claiming orgs.

Revision ID: 0002_org_join_policy
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_org_join_policy"
down_revision = "0001_oss_baseline"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "organizations",
        sa.Column(
            "join_policy",
            sa.String(length=50),
            nullable=False,
            server_default="INVITE_ONLY",
        ),
    )
    op.execute(
        "UPDATE organizations SET join_policy = 'EMAIL_DOMAIN' "
        "WHERE allow_auto_join = true"
    )
    op.drop_column("organizations", "allow_auto_join")
    # Only EMAIL_DOMAIN orgs claim a domain; release any domain held by an org
    # that is not using the EMAIL_DOMAIN policy.
    op.execute(
        "UPDATE organizations SET email_domain = NULL "
        "WHERE join_policy <> 'EMAIL_DOMAIN'"
    )
    # Existing rows are backfilled; the ORM supplies the value on insert.
    op.alter_column("organizations", "join_policy", server_default=None)


def downgrade() -> None:
    op.add_column(
        "organizations",
        sa.Column(
            "allow_auto_join",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.execute(
        "UPDATE organizations SET allow_auto_join = true "
        "WHERE join_policy = 'EMAIL_DOMAIN'"
    )
    op.drop_column("organizations", "join_policy")
    op.alter_column("organizations", "allow_auto_join", server_default=None)
