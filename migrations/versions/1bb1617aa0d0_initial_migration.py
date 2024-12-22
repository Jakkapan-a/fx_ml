"""Initial migration

Revision ID: 1bb1617aa0d0
Revises: 
Create Date: 2024-12-22 17:23:54.795767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bb1617aa0d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forex_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('timeframe', sa.String(length=10), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lstm_file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=False),
    sa.Column('timeframe', sa.String(length=10), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lstm_file')
    op.drop_table('forex_data')
    # ### end Alembic commands ###
