"""Merge two migration heads

Revision ID: 99e1a53304f7
Revises: 54fcc9f6d4ff, d658bb7e54a2
Create Date: 2025-05-31 15:18:57.401927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99e1a53304f7'
down_revision: Union[str, None] = ('54fcc9f6d4ff', 'd658bb7e54a2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass 