from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin

class ApiPermission(BaseMixin, UserstampMixin, TimestampMixin, db.Model):

    __tablename__ = 'api_permission'

    api_name = db.Column(db.String(250), nullable=False)
    api_desc = db.Column(db.String(250), nullable=True)
    method = db.Column(db.String(20), nullable=True)
