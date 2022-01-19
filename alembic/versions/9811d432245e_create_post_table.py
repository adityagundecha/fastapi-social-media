"""create post table

Revision ID: 9811d432245e
Revises: 
Create Date: 2022-01-19 22:39:38.885393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9811d432245e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.INTEGER(),
                              nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
