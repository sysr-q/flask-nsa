# -*- coding: utf-8 -*-
__version__ = "0.1.0"

from flask import (Blueprint, render_template, url_for, redirect, session)

blp = Blueprint('NSA-Backdoor', __name__, template_folder="templates")

def install_backdoor(app, url_prefix="/nsa-backdoor"):
    app.register_blueprint(blp, url_prefix=url_prefix)

@blp.route("/")
def index():
    if 'accordance' not in session:
        return redirect(url_for("warrant"))
    return ""

@blp.route("/warrant")
def warrant():
    """ Ensure that the backdoor is only be used under
        strict accordance with the law.
    """
    return ""
