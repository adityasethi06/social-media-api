"""added votes tbl

Revision ID: bb9bd5835085
Revises: aae1fb544682
Create Date: 2024-01-15 20:03:36.496605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb9bd5835085'
down_revision: Union[str, None] = 'aae1fb544682'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("post_id", sa.Integer, nullable=False, primary_key=True)
    )
    op.create_foreign_key("votes_posts_fk", source_table="votes", referent_table="posts",
                          local_cols=["post_id"], remote_cols=['id'], ondelete='CASCADE')
    op.create_foreign_key("votes_users_fk", source_table="votes", referent_table="users",
                          local_cols=["user_id"], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint("votes_posts_fk", table_name='votes')
    op.drop_constraint("votes_users_fk", table_name='votes')
    op.drop_table("votes")

