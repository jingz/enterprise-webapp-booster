from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin
from datetime import datetime

class FeedEntries(BaseMixin, db.Model):
    __tablename__ = 'feed_entries'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String)
    feed_id = db.Column(db.Integer, db.ForeignKey("feed.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String)
    mark_as_read = db.Column(db.Boolean)
    mark_as_goodnews = db.Column(db.Boolean)
    summary = db.Column(db.String)
    published = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    feed = db.relationship("Feed", backref="entries")

    @classmethod
    def today(cls):
        today_date = datetime.today().date()
        return cls.query.filter_by(published=today_date)

