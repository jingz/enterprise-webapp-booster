from enlighten.controllers import *
from enlighten.models import EltUser

@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/login", methods="POST")
def login():
    print request.args
    return jsonify({'success': True});


# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # For demonstration purposes the password in stored insecurely
#         user = EltUser.query.filter_by(username=form.username.data,
#                                     password=form.password.data).first()
# 
#         if user:
#             login_user(user)
# 
#             flash("Logged in successfully.", "success")
#             return redirect(request.args.get("next") or url_for(".home"))
#         else:
#             flash("Login failed.", "danger")
# 
#     return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))


@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200
