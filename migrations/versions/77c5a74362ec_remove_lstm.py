"""Remove lstm

Revision ID: 77c5a74362ec
Revises: 1bb1617aa0d0
Create Date: 2024-12-22 19:39:21.238986

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '77c5a74362ec'
down_revision = '1bb1617aa0d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lstm_file')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lstm_file',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('symbol', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('timeframe', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('filename', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='lstm_file_pkey')
    )
    # ### end Alembic commands ###
