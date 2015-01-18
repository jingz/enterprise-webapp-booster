from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin

class UserNotAllowPermission(BaseMixin, UserstampMixin, TimestampMixin, db.Model):
    __tablename__ = 'user_not_allow_permission'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('api_permission.id'))

    # user = db.relationship('User')
    # perm = db.relationship('ApiPermission', secondary='api_permission.id')
