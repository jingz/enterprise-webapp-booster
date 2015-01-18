"""add unique constrain

Revision ID: d8af2114f96
Revises: 33f04f6da574
Create Date: 2014-12-22 17:06:26.642416

"""

# revision identifiers, used by Alembic.
revision = 'd8af2114f96'
down_revision = '33f04f6da574'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint(None, 'feed', ['url'])


def downgrade():
    op.drop_constraint(None, 'feed')
