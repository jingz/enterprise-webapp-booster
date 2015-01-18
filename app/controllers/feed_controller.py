from . import *
from app.models import db, Feed

bp = Blueprint('feed_api', __name__)
before_request_extract_page_params(bp)

# prefix feed
@bp.route("/", methods=['GET', 'OPTIONS'])
def index():
    feeds = Feed.search(request.args)
    return render_records(feeds)

@bp.route("/", methods=['POST'])
def create():
    url = request.json.get('url', None)
    print url
    if url:
        r = Feed(url=url, name=url)
        db.session.add(r)
        db.session.commit()
        return render_record(r)
    return render_fail("Cannot Create This Feed")

