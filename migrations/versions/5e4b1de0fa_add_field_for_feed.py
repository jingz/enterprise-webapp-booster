"""add field for feed

Revision ID: 5e4b1de0fa
Revises: 45f416fd8ee5
Create Date: 2014-12-25 19:18:54.585528

"""

# revision identifiers, used by Alembic.
revision = '5e4b1de0fa'
down_revision = '45f416fd8ee5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(u'feed', sa.Column('is_skip', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column(u'feed', 'is_skip')
