"""added Content col to posts table

Revision ID: 5fcb82fb61ff
Revises: 801e9e878e15
Create Date: 2024-01-15 19:34:24.336790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fcb82fb61ff'
down_revision: Union[str, None] = '801e9e878e15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column('content', sa.String, nullable=False))

def downgrade() -> None:
    op.drop_column("posts", "content")
