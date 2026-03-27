"""v1 add user_id fk to posts

Revision ID: 7a01568ebe92
Revises: ec09a7bef720
Create Date: 2026-03-26 19:42:37.002714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a01568ebe92'
down_revision: Union[str, Sequence[str], None] = 'ec09a7bef720'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('user_id', sa.Integer, nullable=False))
    op.create_foreign_key('fk_posts_users', source_table="posts", referent_table="users",
                          local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_posts_users', table_name="posts")
    op.drop_column('posts', 'user_id')
