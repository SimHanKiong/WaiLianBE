"""Change time to time

Revision ID: 09910c78171b
Revises: 28cab067ce29
Create Date: 2025-12-29 22:19:04.972193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09910c78171b'
down_revision: Union[str, None] = '28cab067ce29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('location', sa.Column('time_reach', sa.Time(timezone=False), nullable=True))
    op.execute("""
        UPDATE location 
        SET time_reach = time::time
        WHERE time IS NOT NULL
    """)
    op.alter_column('location', 'time_reach',
                   existing_type=sa.Time(timezone=False),
                   nullable=False)
    op.drop_column('location', 'time')


def downgrade() -> None:
    op.add_column('location', sa.Column('time', sa.String(), nullable=True))
    op.execute("""
        UPDATE location 
        SET time = to_char(time_reach, 'HH12:MI AM')
        WHERE time_reach IS NOT NULL
    """)
    op.alter_column('location', 'time',
                   existing_type=sa.String(),
                   nullable=False)
    op.drop_column('location', 'time_reach')