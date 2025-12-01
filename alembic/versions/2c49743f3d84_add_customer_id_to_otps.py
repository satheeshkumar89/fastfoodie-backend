"""add_customer_id_to_otps

Revision ID: 2c49743f3d84
Revises: add_categories_table
Create Date: 2025-12-01 10:36:27.267970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c49743f3d84'
down_revision: Union[str, Sequence[str], None] = 'add_categories_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('otps', sa.Column('customer_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_otps_customer_id', 'otps', 'customers', ['customer_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_otps_customer_id', 'otps', type_='foreignkey')
    op.drop_column('otps', 'customer_id')
