"""remove tracking user from feed

Revision ID: 33f04f6da574
Revises: 4f5d2cc8e191
Create Date: 2014-12-22 16:23:37.475377

"""

# revision identifiers, used by Alembic.
revision = '33f04f6da574'
down_revision = '4f5d2cc8e191'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column(u'feed', 'updated_by')
    op.drop_column(u'feed', 'created_by')


def downgrade():
    op.add_column(u'feed', sa.Column('created_by', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.add_column(u'feed', sa.Column('updated_by', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
