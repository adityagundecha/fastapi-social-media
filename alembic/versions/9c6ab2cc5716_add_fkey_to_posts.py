"""add fkey to posts

Revision ID: 9c6ab2cc5716
Revises: 9da0f4badb22
Create Date: 2022-01-21 22:36:35.041149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c6ab2cc5716'
down_revision = '9da0f4badb22'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('posts_users,fk', table_name='posts')
    op.drop_column('posts', 'owner_id')