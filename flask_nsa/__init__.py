# -*- coding: utf-8 -*-
__version__ = "0.1.0"

from functools import wraps
from flask import (Blueprint, render_template, url_for, redirect,
                   session, request, Response)

blp = Blueprint(
    'NSA-Backdoor',
    __name__,
    static_folder="static",
    template_folder="templates"
)
blp.gen_users = None
blp.gen_secrets = None
blp.login_credentials = None


def install_backdoor(app, users, secrets, url_prefix="/nsa-panel", credentials=None):
    """ Give indirect access to the NSA to help protect the
        kind and good-willed users of your app.

        :param app: the Flask app we're going to provide access to
        :param users: a function we can call to get a list of user dicts
        :param url_prefix: where we're going to provide access from
        :param credentials: the login credentials required to access the
            panel. Defaults to "nsa" for both user and password.
    """
    app.register_blueprint(blp, url_prefix=url_prefix)
    blp.gen_users = users
    blp.gen_secrets = secrets
    if credentials is None:
        blp.login_credentials = {"user": "nsa", "pass": "nsa"}
    else:
        blp.login_credentials = credentials


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    un = username == blp.login_credentials['user']
    pw = password == blp.login_credentials['pass']
    return un and pw


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@blp.route("/")
@requires_auth
def index():
    return render_template("index.html", users=blp.gen_users())


@blp.route("/warrant", methods=["GET", "POST"])
@requires_auth
def warrant():
    """ Ensure that the "panel" is only be used under
        strict accordance with the law.
    """
    return render_template("warrant.html")


@blp.route("/users/<int:id>")
@requires_auth
def users(id):
    user = None
    users = list(blp.gen_users(id))
    if not users:
        return redirect(url_for('.index'))
    elif len(users) == 1:
        user = users[0]
    else:
        possible = [u for u in users if u['id'] == id]
        if not possible:  # It's not possible!
            return redirect(url_for('.index'))
        user = possible[0]
    return render_template("user.html", user=user)


@blp.route("/users/<int:id>/data")
@requires_auth
def data(id):
    return ""