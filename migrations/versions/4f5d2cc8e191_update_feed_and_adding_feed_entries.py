"""update feed and adding feed entries

Revision ID: 4f5d2cc8e191
Revises: 595d4d76ce39
Create Date: 2014-12-22 16:21:35.853533

"""

# revision identifiers, used by Alembic.
revision = '4f5d2cc8e191'
down_revision = '595d4d76ce39'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('feed_entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.String(), nullable=True),
    sa.Column('feed_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('link', sa.String(), nullable=True),
    sa.Column('summary', sa.String(), nullable=True),
    sa.Column('published', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column(u'feed', 'etag',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column(u'feed', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column(u'feed', 'status',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade():
    op.alter_column(u'feed', 'status',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column(u'feed', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column(u'feed', 'etag',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_table('feed_entries')
