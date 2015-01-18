from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin

class RolePermission(BaseMixin, UserstampMixin, TimestampMixin, db.Model):

    #-#-#-#-#---------------------------------------------------------
    __tablename__ = 'role_permission'

    # role_id: reference to elt role
    role_id = db.Column(db.Integer)

    # permission_type: type of permission
    #   1) Group Permission     --> G
    #   2) Detail Permission    --> P
    permission_type = db.Column(db.String(1), nullable=False)

    # permission_name: permission name (permission group name or permission 
    #   name depending on permission_type field
    permission_name = db.Column(db.String(50), nullable=False)
    #-#-#-#-#---------------------------------------------------------
