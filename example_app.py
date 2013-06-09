# -*- coding: utf-8 -*-
""" This is an example application demonstrating the
    NSA ~~Backdoor~~ *ahem*, sorry, "Panel".

    It's really this easy to protect your users from
    possible threats of terror (or privacy) online!
"""
import random
import sys

from flask import Flask
from flask_nsa import install_backdoor

def gen_users(id=None):
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
    yield {
        "id": 0,
        "name": "John Smith",
        "creation": "__blackout__",
        "friends": 10
    }
    yield {
        "id": 1,
        "name": "Jane Smith",
        "creation": "__blackout__",
        "friends": 2  # Nobody loves Jane. :'(
    }
    yield {
        "id": 2,
        "name": "Little Bobby Tables",
        "creation": "__blackout__",
        "friends": 7
    }
    yield {
        "id": 3,
        "name": "Elaine Roberts",
        "creation": "__blackout__",
        "friends": 5
    }

def gen_secrets():
    """ Purely a hypothetical example; you should provide
        the NSA with the __real__ secrets of your users.

        This simply generates 25 secrets per user from
        the above users() function. Static numbers are fun.
    """
    for u in xrange(0, 4):
        for i in xrange(0, 25):
            yield {
                "id": i,
                "uid": u,
                "secret": "Something that should not be seen."
            }

def gen_friends():
    """ Another hypothetical example, with a small subset
        of names.

        If only the real world would let you make friends
        with a generator statement, eh?
    """
    fnames = ["John", "Jane", "Mary", "Kate", "Ashleigh",
              "Chris", "Timothy", "Bobby", "Maxwell", "Amy"]
    lnames = ["Smith", "Hansen", "Carter", "Macky", "Hull",
              "Richards", "Chan", "Cameron", "Sharp", "Dicken"]
    for u in gen_users():
        for i in xrange(0, u['friends']):
            yield {
                "id": i,
                "uid": u['id'],
                "name": "{0} {1}".format(
                    random.choice(fnames),
                    random.choice(lnames)
                )
            }

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "NSA_ROX!"
    app.debug = "--debug" in sys.argv
    install_backdoor(app, gen_users, secrets=gen_secrets, friends=gen_friends)
    app.run()
