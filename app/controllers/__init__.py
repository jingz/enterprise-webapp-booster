from flask import (Blueprint, 
                   request, 
                   url_for, 
                   jsonify,
                   session,
                   send_file,
                   Response)

from flask.ext.login import login_user, logout_user, login_required
from app import cache
import re

# controller helpers

# api protocal
common_params = {}
def before_request_extract_page_params(blueprint):
    @blueprint.before_request
    def __extract():
        page = int(request.args.get('page', '1'))
        limit = int(request.args.get('limit', '20'))
        start = int(request.args.get('start', '0'))
        common_params['page'] = page
        common_params['limit'] = limit
        common_params['offset'] = start

def before_request_extract_inquiry_params(blueprint):
    @blueprint.before_request
    def __extract():
        __model = request.args.get('model', None)

def require_authenticated(blueprint, except_actions=[]):
    @blueprint.before_request
    def check_permission():
        tag = "%s_%s" % (request.method.lower(), request.path.lower().strip('/'))
        perms = session.get('perms', {})
        print '@' * 70
        print request.path
        print request.method
        print tag
        print perms
        print '@' * 70
        #return Response("won't let you get in!", status=403)
        if tag in ('post_login', 'get_logout'):
            return
        if not tag in perms:
            return Response(status=403)
        return

# render helper for extjs
def render_records(alc_objects):
    print common_params
    data = [o.to_dict() for o in
            alc_objects.limit(common_params['limit']).offset(common_params['offset'])]
    di = { 'data': data, 'total': alc_objects.count(), 'success': True }
    return jsonify(di)

def render_record(alc_object, message=None):
    di = { 'record': alc_object.to_dict(), 'success': True }
    if message:
        di['message'] = message
    return jsonify(di)

def render_fail(msg):
    return jsonify({ 'message': msg, 'success': False})

def render_success(msg):
    return jsonify({ 'message': msg, 'success': True})

def extract_sort_params(d):
    for k, v in d.items():
        print k, v
    print d
    return "title asc"
