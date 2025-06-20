"""Add password to school

Revision ID: 405266c66f60
Revises: cc8bf15c1820
Create Date: 2025-06-15 20:46:39.177956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '405266c66f60'
down_revision: Union[str, None] = 'cc8bf15c1820'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('school', sa.Column('password', sa.String(), nullable=False, server_default=''))
    op.alter_column('school', 'password', server_default=None)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('school', 'password')
    # ### end Alembic commands ###
