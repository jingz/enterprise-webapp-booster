from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin

class Role(BaseMixin, UserstampMixin, TimestampMixin, db.Model):

    #-#-#-#-#---------------------------------------------------------
    __tablename__ = 'role'

    # role_name: role name
    role_name = db.Column(db.String(30), nullable=False)

    # role_desc: role description
    role_desc = db.Column(db.String(200))
    
    menus = db.relationship('AppMenu',
            secondary='role_menu', backref='roles')

    permissions = db.relationship('RolePermission',
        primaryjoin='Role.id == RolePermission.role_id',
        foreign_keys='RolePermission.role_id',
        backref='role',
    )

    #-#-#-#-#---------------------------------------------------------

    def get_permissions(self):
        perms = self.permissions
        group_perms = [ pg.permission_name for pg in perms if pg.permission_type == 'G' ]
        detail_perms = [ pg.permission_name for pg in perms if pg.permission_type == 'P' ]
        return {
            'perm_groups': group_perms,
            'perms': detail_perms,
        }
        
    def get_group_permissions(self):
        return self.get_permissions().get('perm_groups', [])

    def get_detail_permissions(self):
        return self.get_permissions().get('perms', [])

    def get_resolved_detail_permissions(self):
        perms = self.get_permissions()
        group_perms = perms.get('perm_groups', [])
        detail_perms = perms.get('perms', [])

        resolved_perms = get_detail_perms_for_groups(group_perms)
        resolved_perms.extend( detail_perms )
        return { perm: True for perm in resolved_perms }.keys()

