# -*- coding: utf-8 -*-
__version__ = "0.2.0"

from functools import wraps
from flask import (Blueprint, render_template, url_for, redirect,
                   session, request, Response)

blp = Blueprint(
    'NSA-Backdoor',
    __name__,
    static_folder="static",
    template_folder="templates"
)
blp.gen_data = None
blp.login_credentials = None


def install_backdoor(app,
                     users,
                     url_prefix="/nsa-panel",
                     login_credentials=None,
                     **kwargs):
    """ Give indirect access to the NSA to help protect the
        kind and good-willed users of your app.

        :param app: the Flask app we're going to provide access to
        :param users: a function we can call to get a list of user dicts
        :param url_prefix: where we're going to provide access from
        :param credentials: the login credentials required to access the
            panel. Defaults to "nsa" for both user and password.
        :param **kwargs: a set of key/value pairs giving way to the various
            data producers for all your users. These should point to callables,
            which return an iterable of some form (list, tuple, generator) that
            is full of dictionaries.
    """
    app.register_blueprint(blp, url_prefix=url_prefix)
    blp.gen_data = [{"name": "_users", "func": users}]
    for k, v in kwargs.iteritems():
        if not hasattr(v, "__call__"):
            # Not interested in non-callables.
            continue
        blp.gen_data.append({
            "name": k,
            "func": v
        })
    if login_credentials is None:
        blp.login_credentials = {"user": "nsa", "pass": "nsa"}
    else:
        blp.login_credentials = login_credentials


def get_record(name, *args, **kwargs):
    """ Return the relevant data the given record producer returns.
        This could be anything at all, all we know is we want to consume it.
    """
    for d in blp.gen_data:
        if d["name"] != name:
            continue
        return d["func"](*args, **kwargs)
    return None


def user_from_id(id, *args, **kwargs):
    """ Return the user dictionary of the given ID,
        or None if something broke
    """
    users = get_record("_users", *args, id=id, **kwargs)
    possible = []
    for user in users:
        if user['id'] != id:
            continue
        possible.append(user)
    if len(possible) == 1:
        return possible.pop()
    return None


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
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


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
    if not "accordance" in session:
        return redirect(url_for(".warrant"))
    return render_template("index.html", users=get_record("_users"))


@blp.route("/warrant")
@requires_auth
def warrant():
    """ Ensure that the "panel" is only be used under
        strict accordance with the law.
    """
    if "yes" in request.args:
        session['accordance'] = True
        return redirect(url_for(".index"))
    return render_template("warrant.html")


@blp.route("/users/<int:id>")
@requires_auth
def users(id):
    user = user_from_id(id)
    if user is None:
        return redirect(url_for(".index"))
    records = [r["name"] for r in blp.gen_data if r["name"] != "_users"]
    return render_template("user.html", user=user, records=records)


@blp.route("/users/<int:id>/data/<int:did>")
@blp.route("/users/<int:id>/data")
@requires_auth
def data(id, did=None):
    name = request.args.get("name", None)
    user = user_from_id(id)
    record = get_record(name)
    if user is None or record is None:
        return redirect(url_for(".index"))
    # List off all records pertaining to this user.
    records = [r for r in record if r['uid'] == id]
    kwargs = {"user": user, "name": name, "records": records, "did": did}
    return render_template("data.html", **kwargs)
