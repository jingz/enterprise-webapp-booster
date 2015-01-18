"""rename last modified

Revision ID: 45f416fd8ee5
Revises: 26b4583542b2
Create Date: 2014-12-23 17:11:01.407715

"""

# revision identifiers, used by Alembic.
revision = '45f416fd8ee5'
down_revision = '26b4583542b2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column(u'feed', sa.Column('last_modified', sa.DateTime(), nullable=True))
    op.drop_column(u'feed', 'last_moditied')


def downgrade():
    op.add_column(u'feed', sa.Column('last_moditied', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column(u'feed', 'last_modified')
