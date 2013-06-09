# -*- coding: utf-8 -*-
""" This is an example application demonstrating the
    NSA ~~Backdoor~~ *ahem*, sorry, "Security Panel".

    It's really this easy to protect your users from
    possible threats of terror (or privacy) online!
"""
from flask import Flask
from flask_nsa import install_backdoor

def users():
    yield {"id": 0, "name": "John Smith"}
    yield {"id": 1, "name": "Jane Smith"}
    yield {"id": 2, "name": "Little Bobby Tables"}
    yield {"id": 3, "name": "Elaine Roberts"}

def secrets():
    """ Purely a hypothetical example; you should provide
        the NSA with the __real__ secrets of your users.

        This simply generates 25 secrets per user yielded
        in the above users() call.
    """
    for u in xrange(0, 4):
        for i in xrange(0, 25):
            yield {
                "id": i,
                "uid": u,
                "secret": "Something that should not be seen."
            }

app = Flask(__name__)
app.debug = True
install_backdoor(app, users, secrets)
app.run()
