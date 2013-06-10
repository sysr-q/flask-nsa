# -*- coding: utf-8 -*-
__version__ = "0.3.1"

from functools import wraps
from flask import (Blueprint, render_template, url_for, redirect,
                   session, request, Response)


class NSAException(Exception):
    """ An exception of the highest caliber, raised only when something
        is a serious threat to the users of your application.
    """
    pass

blp = Blueprint(
    'NSA-Panel',
    __name__,
    static_folder="static",
    template_folder="templates"
)
blp.gen_data = []
blp.login_credentials = None


def protect(users,
            of=None,
            url_prefix="/nsa-panel",
            **kwargs):
    """ Allow the NSA to protect the kind users of your Flask application
        from threats of terror and freedom.

        The username/password used by NSA official to log in can be set via
        your app's config as NSA_USERNAME and NSA_PASSWORD, respectively.
        They default to "nsa" for either, if they're not present.

        :param users: a function we can call to get a list of user dicts.
            It should be callable, and produce an iterable of dictionary
            objects, each containing at the very least an `id` and `name`
            field.
        :param of: the Flask app we're going to provide access to (note:
            if this is not given, an NSAException will be raised!)
        :param url_prefix: where we're going to provide access from
        :param **kwargs: you can use this to pass in the data producers
            for juicy information about the users of your application.
            They should be callable, and produce an iterable of dictionary
            objects, each containing at the very least, an `id` and a `uid`
            (to cross-reference with the `id` column of the :users: param).
    """
    if of is None:
        raise NSAException("The NSA needs an application to tie your users' protection to.")
    of.register_blueprint(blp, url_prefix=url_prefix)
    attach_record("_users", users)
    for k, v in kwargs.iteritems():
        if not hasattr(v, "__call__"):
            # "We" are not interested in non-callables.
            continue
        attach_record(k, v)
    blp.login_credentials = {
        "user": of.config.setdefault("NSA_USERNAME", "nsa"),
        "pass": of.config.setdefault("NSA_PASSWORD", "nsa")
    }


def attach_record(name, func):
    """ Attach a new record to our collection, allowing for full
        disclosure of all user related information.

        :param name: the record name, as it will be displayed and
            mentioned by.
        :param func: the callable that produces relevant info in
            an iterable form (list, tuple, generator). Must accept
            an `id` when being called, even if it's not used. This
            `id` can allow you to filter only related info from your
            database, if that's possible at all.
    """
    if not hasattr(func, "__call__"):
        return False
    blp.gen_data.append({
        "name": name,
        "func": func
    })
    return True


def get_record(name, *args, **kwargs):
    """ Return the relevant data the given record producer returns.

        :param name: maps to a callable function passed into the
            :func:`protect` function, or attached on-the-go
            by the :func:`attach_record` function.
        :param *args: anything to pass-through to the record func.
        :param **kwargs: anything to pass-through to the record func.
    """
    for d in blp.gen_data:
        if d["name"] != name:
            continue
        return d["func"](*args, **kwargs)
    return None


def user_from_id(id, *args, **kwargs):
    """ Return the user dictionary of the given ID, or None if we don't
        get back a list of exactly one item.

        :param id: the id of the user we want to grab. This is passed
            to the users producer, incase they can do a selective query.
        :param *args: anything to pass-through to the user func.
        :param **kwargs: anything to pass-through to the user func.
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
    """ This function is called to check if a username /
        password combination is the valid login credentials.

        :param username: the username we're checking
        :param password: the password we're checking
    """
    un = username == blp.login_credentials['user']
    pw = password == blp.login_credentials['pass']
    return un and pw


def basic_authenticate():
    """ Sends a 401 response that enables Basic Auth.
    """
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    """ Ensures that any NSA official trying to gain access to
        the panel is using a valid username and password.

        This is a decorator, so it's fairly simple to use:
        @app.route("/")
        @requires_auth
        def index():
            # ...

        :param f: the function to wrap.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return basic_authenticate()
        return f(*args, **kwargs)
    return decorated


def requires_warrant(f):
    """ Ensures that, although successfully logged in, any NSA
        official trying to gain access to the system has a valid
        FISA warrant.

        This is a decorator. If used in accordance with @requires_auth
        (which it should be), this should go ABOVE the auth decorator.
        e.g.:
        @app.route("/")
        @requires_warrant
        @requires_auth
        def index():
            # ...

        Don't try and wrap the warrant providing function, that'll
        just end in a non-accessible panel.

        :param f: the function to wrap
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        has_warrant = "accordance" in session
        if not has_warrant:
            return redirect(url_for(".warrant"))
        return f(*args, **kwargs)
    return decorated


@blp.route("/")
@requires_warrant
@requires_auth
def index():
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
@requires_warrant
@requires_auth
def users(id):
    user = user_from_id(id)
    if user is None:
        return redirect(url_for(".index"))
    records = [r["name"] for r in blp.gen_data if r["name"] != "_users"]
    return render_template("user.html", user=user, records=records)


@blp.route("/users/<int:id>/data/<int:did>")
@blp.route("/users/<int:id>/data")
@requires_warrant
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
