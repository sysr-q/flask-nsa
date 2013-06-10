# -*- coding: utf-8 -*-
""" This is an example application demonstrating the
    NSA ~~Backdoor~~ *ahem*, sorry, "Panel".

    It's really this easy to protect your users from
    possible threats of terror (or privacy) online!
"""
import random
import sys

from flask import Flask
from flask.ext import nsa


def users(id=None):
    """ Pull and yield all of the relevant information
        about your application's users.

        This should return an iterable of dictionaries. Each
        of these should contain (at the very least), an `id`
        and a `name`. Anything else is simply displayed as relevant
        information in the panel.

        If you set any of the fields to a value of "__blackout__",
        it will be displayed instead as a black block of blank text.

        :param id: an optional (e.g. you don't have to use it)
            id that you can use to filter queries. This is based
            on the `id` column of whatever you provide.
    """
    return [
        {
            "id": 0,
            "name": "John Smith",
            "creation": "__blackout__",
            "friends": 10
        },
        {
            "id": 1,
            "name": "Jane Smith",
            "creation": "__blackout__",
            "friends": 2  # Nobody loves Jane. :'(
        },
        {
            "id": 2,
            "name": "Little Bobby Tables",
            "creation": "__blackout__",
            "friends": 7
        },
        {
            "id": 3,
            "name": "Elaine Roberts",
            "creation": "__blackout__",
            "friends": 5
        }
    ]


def gen_secrets():
    """ Purely a hypothetical example; you should provide
        the NSA with the __real__ secrets of your users.

        This simply generates 25 secrets per user from
        the above users() function. Static numbers are fun.

        This yields, simply to show that any iterable return
        works in the NSA panel. Be it list or a generator.
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
    for u in users():
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
    nsa.protect(users, of=app, secrets=gen_secrets, friends=gen_friends)
    app.run()
