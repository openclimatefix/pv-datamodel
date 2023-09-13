"""add api request table

Revision ID: d60cb99ff9e6
Revises: c7aef501056e
Create Date: 2023-09-13 09:10:27.741808

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd60cb99ff9e6'
down_revision = 'c7aef501056e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_request',
    sa.Column('created_utc', sa.DateTime(), nullable=True),
    sa.Column('uuid', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('user_uuid', postgresql.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.user_uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_api_request_user_uuid'), 'api_request', ['user_uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_api_request_user_uuid'), table_name='api_request')
    op.drop_table('api_request')
    # ### end Alembic commands ###
