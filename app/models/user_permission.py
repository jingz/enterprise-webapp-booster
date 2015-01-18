from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin

class UserPermission(BaseMixin, UserstampMixin, TimestampMixin, db.Model):

    __tablename__ = 'user_permission'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('api_permission.id'))
