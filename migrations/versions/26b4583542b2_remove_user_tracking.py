"""remove user tracking

Revision ID: 26b4583542b2
Revises: 2dc74fab7190
Create Date: 2014-12-23 17:05:04.788858

"""

# revision identifiers, used by Alembic.
revision = '26b4583542b2'
down_revision = '2dc74fab7190'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column(u'feed_entries', 'updated_by')
    op.drop_column(u'feed_entries', 'created_by')


def downgrade():
    op.add_column(u'feed_entries', sa.Column('created_by', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.add_column(u'feed_entries', sa.Column('updated_by', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
