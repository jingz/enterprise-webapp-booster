from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin

class UserRole(BaseMixin, UserstampMixin, TimestampMixin, db.Model):

    #-#-#-#-#---------------------------------------------------------
    __tablename__ = 'user_role'

    # user_id: reference to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # role_id: reference to role
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    #-#-#-#-#---------------------------------------------------------
