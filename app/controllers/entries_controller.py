# -*- coding: utf-8 -*-
from . import *
from app.models import db, Feed, FeedEntries

bp = Blueprint('entries_api', __name__)
before_request_extract_page_params(bp)

# prefix feed
@bp.route("/", methods=['GET', 'OPTIONS'])
def index():
    params = request.args.copy()
    # params.update({'title_contains': 'ซึ้ง'})
    feeds = FeedEntries.search(params).filter("mark_as_read is not true").order_by('published desc')
    return render_records(feeds)

# update all
@bp.route("/chunk", methods=['PUT'])
def update_all():
    # record to update
    records = request.json.get('records', None) 
    print records
    for r in records:
        _rec = FeedEntries.query.get(r.pop('id'))
        _rec.update_all(r)
        db.session.add(_rec)
    db.session.commit()
    return render_success("All records has been updated"); 
