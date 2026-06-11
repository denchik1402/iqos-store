"""Season collection flags on product

Revision ID: 011
Revises: 010
Create Date: 2026-06-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '011'
down_revision: Union[str, None] = '010'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('product') as batch_op:
        batch_op.add_column(sa.Column('is_season', sa.Boolean(), nullable=True, server_default=sa.false()))
        batch_op.add_column(sa.Column('season_sort_order', sa.Integer(), nullable=True, server_default='0'))
        batch_op.add_column(sa.Column('season_excluded', sa.Boolean(), nullable=True, server_default=sa.false()))


def downgrade() -> None:
    with op.batch_alter_table('product') as batch_op:
        batch_op.drop_column('season_excluded')
        batch_op.drop_column('season_sort_order')
        batch_op.drop_column('is_season')
