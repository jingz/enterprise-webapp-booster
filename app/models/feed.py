from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin

class Feed(BaseMixin, TimestampMixin, db.Model):
    __tablename__ = 'feed'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String)
    etag = db.Column(db.String)
    status = db.Column(db.Integer)
    is_skip = db.Column(db.Boolean)
    last_modified = db.Column(db.DateTime)
