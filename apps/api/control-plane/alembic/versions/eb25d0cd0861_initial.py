"""initial

Revision ID: eb25d0cd0861
Revises: 
Create Date: 2026-07-21 12:54:26.373285

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'eb25d0cd0861'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
