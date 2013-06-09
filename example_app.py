# -*- coding: utf-8 -*-
""" This is an example application demonstrating the
    NSA ~~Backdoor~~ *ahem*, sorry, "Panel".

    It's really this easy to protect your users from
    possible threats of terror (or privacy) online!
"""
from flask import Flask
from flask_nsa import install_backdoor

def users(id=None):
    """ Pull and yield all of the relevant information
        about your application's users.

        Provide a dictionary with at the very least their
        `id` and `name`. Anything extra you provide will be
        shown in the user info table, so make sure **not**
        to redact completely private and confidential info
        from the NSA.
        Alternatively, return "__blackout__" and it will
        magically transform into a black text block.

        Oh, and if you can pull just one user's data based
        on a given `id`, that'd be really helpful. Otherwise,
        just assign it to None, since it will still be called.
    """
    yield {"id": 0, "name": "John Smith", "age": "__blackout__"}
    yield {"id": 1, "name": "Jane Smith", "age": "__blackout__"}
    yield {"id": 2, "name": "Little Bobby Tables", "age": "__blackout__"}
    yield {"id": 3, "name": "Elaine Roberts", "age": "__blackout__"}

def secrets():
    """ Purely a hypothetical example; you should provide
        the NSA with the __real__ secrets of your users.

        This simply generates 25 secrets per user from
        the above users() function.
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
