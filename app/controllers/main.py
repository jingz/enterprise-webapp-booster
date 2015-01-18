import json
from flask import Blueprint, render_template, flash, request, redirect, url_for, make_response, session, current_app, Response 
# from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.principal import Identity, identity_changed
from app import cache
from app.models import User
from app.models import AppMenu
from . import jsonify, render_fail
from functools import wraps

main = Blueprint('main', __name__)

# simple decorator for require login
def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') is None:
            if request.is_xhr:
                return Response(status=401)
            else:
                return redirect(url_for('.login'))

        u = session.get('user')
        u = User.query.get(u.id)
        endpoint, method = request.endpoint, request.method
        print u.username, endpoint, method
        # TODO cache permissions
        allow_access = False
        for perm in u.perms:
            if perm.api_name == endpoint and perm.method == method:
                allow_access = True

        if not allow_access:
            return Response(status=403)

        return func(*args, **kwargs)
    return wrapper

# simple access control list by role
def acl(role_list=[]):
    def acl_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            u = session.get('user')
            u = User.query.get(u.id) # refresh user
            u.roles
            return func(*args, **kwargs)
        return wrapper
    return acl_decorator

# @cache.cached(timeout=1000)
@main.route('/')
@require_login
def home():
    u = session.get('user')
    # retrive user
    u = User.query.get(u.id)
    lmenu = u.get_menu_list()
    tree_formatter = lambda m, children: { 'text': m.text, 'href': m.url, 'leaf': (True if len(children) == 0 else False) }
    menu_tree = AppMenu.build_menu_tree(lmenu, formatter=tree_formatter)
    menu_list = [menu.to_dict() for menu in lmenu]
    menu_urls = [menu.url for menu in lmenu if menu.url is not None]
    return render_template('index.html', 
                            menu_tree=menu_tree, 
                            menu_urls=menu_urls)

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("extjs_login.html")

    # print request.get_json()
    # print request.form
    user = request.json.pop('username', None)
    pwd = request.json.pop('password', None)
    if user and pwd:
        u = User.authenticate(user, pwd)

        if u:
            # setup session
            session['user'] = u
            # get_some_uri
            session['perm'] = [ p.api_name for p in u.perms ]
            # redirect to home
            return jsonify({'success': True, 'url': '/'})

    return render_fail('Wrong! username or password')

@main.route('/logout')
@require_login
def logout():
    session.pop('user', None)
    return redirect(url_for('.login'))

"""
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            result = login_user(user)

            flash("Logged in successfully.", "success")
            #return redirect(request.args.get("next") or url_for(".home"))
            if result:
                session['menu'] = json.dumps(user.get_menu(), indent=2)

                # init flask-principal identity and needs
                #identity_changed.send(
                #    current_app._get_current_object(),
                #    identity=Identity(user.id)
                #)
                session['perms'] = { perm: True for perm in user.get_all_detail_permissions() }
                return make_response('login success')
            else:
                return make_response('user inactive')
        else:
            #flash("Login failed.", "danger")
            #return redirect(request.args.get("next") or url_for(".home"))
            return make_response('login failed')

    return render_template("login.html", form=form)

@main.route("/restricted", methods=['GET'])
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200

@main.route("/xxx")
#@perm.perm_lst_xxx.require(http_exception=403)
def list_xxx():
    return "listing xxx", 200

@main.route("/yyy")
#@perm.perm_lst_yyy.require(http_exception=403)
def list_yyy():
    return "listing yyy", 200

@main.errorhandler(403)
def authorization_failed(e):
    return "authorization failed", 403

"""
