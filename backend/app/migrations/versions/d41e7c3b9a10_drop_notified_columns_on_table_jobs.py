"""drop telegram_notified and discord_notified columns on table jobs

Revision ID: d41e7c3b9a10
Revises: 02e9dcf05ee9
Create Date: 2026-11-13 05:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd41e7c3b9a10'
down_revision: Union[str, Sequence[str], None] = '02e9dcf05ee9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('jobs', 'telegram_notified')
    op.drop_column('jobs', 'discord_notified')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('jobs', sa.Column('discord_notified', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('jobs', sa.Column('telegram_notified', sa.Boolean(), server_default='false', nullable=False))
