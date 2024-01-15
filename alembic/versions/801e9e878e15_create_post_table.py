"""create post table

Revision ID: 801e9e878e15
Revises: 
Create Date: 2024-01-15 19:26:55.186050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '801e9e878e15'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('title', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_table("posts")
