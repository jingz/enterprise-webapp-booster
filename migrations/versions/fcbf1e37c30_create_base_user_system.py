"""create base user system

Revision ID: fcbf1e37c30
Revises: None
Create Date: 2014-12-06 16:51:53.091407

"""

# revision identifiers, used by Alembic.
revision = 'fcbf1e37c30'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_name', sa.String(length=30), nullable=False),
    sa.Column('role_desc', sa.String(length=200), nullable=True),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('api_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_name', sa.String(length=250), nullable=False),
    sa.Column('api_desc', sa.String(length=250), nullable=True),
    sa.Column('method', sa.String(length=20), nullable=True),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('permission_type', sa.String(length=1), nullable=False),
    sa.Column('permission_name', sa.String(length=50), nullable=False),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('branch_id', sa.Integer(), nullable=True),
    sa.Column('soft_password_expiration_date', sa.Date(), nullable=True),
    sa.Column('hard_password_expiration_date', sa.Date(), nullable=True),
    sa.Column('failed_login_count', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=1), nullable=False),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('app_menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_not_allow_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['api_permission.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role_menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['app_menu.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.Column('updated_by', sa.String(length=20), nullable=False),
    sa.Column('created_by', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['api_permission.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('user_permission')
    op.drop_table('user_role')
    op.drop_table('role_menu')
    op.drop_table('user_not_allow_permission')
    op.drop_table('app_menu')
    op.drop_table('user')
    op.drop_table('role_permission')
    op.drop_table('api_permission')
    op.drop_table('role')
