from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin

class RoleMenu(BaseMixin, UserstampMixin, TimestampMixin, db.Model):
    __tablename__ = 'role_menu'

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('app_menu.id'))

    role = db.relationship('Role')
    menu = db.relationship('AppMenu')
