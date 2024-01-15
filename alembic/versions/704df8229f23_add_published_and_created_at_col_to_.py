"""add published and created_at col to posts tbl

Revision ID: 704df8229f23
Revises: 5fcb82fb61ff
Create Date: 2024-01-15 19:38:49.902182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '704df8229f23'
down_revision: Union[str, None] = '5fcb82fb61ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column('published', sa.Boolean, nullable=False, server_default='True'))
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
