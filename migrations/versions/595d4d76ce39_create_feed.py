"""create feed

Revision ID: 595d4d76ce39
Revises: fcbf1e37c30
Create Date: 2014-12-21 14:51:19.097577

"""

# revision identifiers, used by Alembic.
revision = '595d4d76ce39'
down_revision = 'fcbf1e37c30'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('feed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('etag', sa.String(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('feed')
