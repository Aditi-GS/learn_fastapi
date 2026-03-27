"""v1 create votes table

Revision ID: e30ac7fa96d2
Revises: 7a01568ebe92
Create Date: 2026-03-26 19:49:56.337941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e30ac7fa96d2'
down_revision: Union[str, Sequence[str], None] = '7a01568ebe92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('votes',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_votes_posts'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_votes_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id', name=op.f('votes_pkey'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('votes')