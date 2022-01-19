"""Add content column to posts

Revision ID: 954ee4e7fddc
Revises: 9811d432245e
Create Date: 2022-01-19 22:54:29.800401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '954ee4e7fddc'
down_revision = '9811d432245e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
