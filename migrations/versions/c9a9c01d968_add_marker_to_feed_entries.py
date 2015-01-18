"""add marker to feed entries

Revision ID: c9a9c01d968
Revises: 5e4b1de0fa
Create Date: 2014-12-27 14:58:26.027712

"""

# revision identifiers, used by Alembic.
revision = 'c9a9c01d968'
down_revision = '5e4b1de0fa'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(u'feed_entries', sa.Column('mark_as_goodnews', sa.Boolean(), nullable=True))
    op.add_column(u'feed_entries', sa.Column('mark_as_read', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column(u'feed_entries', 'mark_as_read')
    op.drop_column(u'feed_entries', 'mark_as_goodnews')
