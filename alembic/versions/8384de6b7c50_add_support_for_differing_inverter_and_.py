"""Add support for differing inverter and module capacities

Revision ID: 8384de6b7c50
Revises: aeea08bcfc42
Create Date: 2023-04-08 12:26:23.042938

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8384de6b7c50'
down_revision = 'aeea08bcfc42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('sites', 'capacity_kw', new_column_name='inverter_capacity_kw')
    op.add_column('sites', sa.Column('module_capacity_kw', sa.Float(), nullable=True, comment='The PV module nameplate capacity of the site'))


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sites', 'inverter_capacity_kw', new_column_name='capacity_kw')
    op.drop_column('sites', 'module_capacity_kw')
    
