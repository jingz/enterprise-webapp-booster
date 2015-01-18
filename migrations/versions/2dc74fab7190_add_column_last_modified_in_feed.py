"""add column last modified in feed

Revision ID: 2dc74fab7190
Revises: d8af2114f96
Create Date: 2014-12-23 12:21:23.902187

"""

# revision identifiers, used by Alembic.
revision = '2dc74fab7190'
down_revision = 'd8af2114f96'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(u'feed', sa.Column('last_moditied', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column(u'feed', 'last_moditied')
