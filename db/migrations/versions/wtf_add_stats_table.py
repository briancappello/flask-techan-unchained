from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'wtf'
down_revision = 'f1fa43982725'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "stats",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("day", sa.Date(), nullable=False),
        sa.Column(
            "freq",
            sa.Enum(
                "min_1",
                "min_2",
                "min_5",
                "min_10",
                "min_15",
                "min_30",
                "hour",
                "day",
                "week",
                "month",
                "quarter",
                "year",
                name="freq",
            ),
            nullable=False,
        ),
        sa.Column("stats", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_stats")),
        sa.UniqueConstraint("symbol", "day", "freq", name="uq_stats_symbol"),
    )
    op.create_index(op.f("ix_stats_day"), "stats", ["day"], unique=False)
    op.create_index(op.f("ix_stats_freq"), "stats", ["freq"], unique=False)
    op.create_index(op.f("ix_stats_symbol"), "stats", ["symbol"], unique=False)

def downgrade():
    op.drop_index(op.f("ix_stats_day"), table_name="stats")
    op.drop_index(op.f("ix_stats_freq"), table_name="stats")
    op.drop_index(op.f("ix_stats_symbol"), table_name="stats")
    op.drop_table("stats")
