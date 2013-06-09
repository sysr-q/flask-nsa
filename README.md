Flask-NSA
=========
![](nsa-eagle.png)

Let the NSA protect the freedom of the users of your Flask app. Feel like ~~destroying all freedom online~~ fighting terror? I sure do!

Example
=======
To see example usage, check out `example_app.py`.

+ `python example_app.py`
+ Visit [127.0.0.1:5000/nsa-panel](http://127.0.0.1:5000/nsa-panel) (use `nsa`/`nsa` to login)

Install
=======

Install it via the conventional means:
```shell
$ git clone https://github.com/plausibility/flask-nsa.git
$ python setup.py install
```

Import `install_backdoor` into your app:
```python
from flask.ext.nsa import install_backdoor
```

Pass `install_backdoor` your app, as well as a generator for your user table and their secrets (which should be public).  
For an example of what you could do, check out `example_app.py`
```python
install_backdoor(app, users, secrets)
```

Send your users the following ~~lie~~ factual statement:

> Dear X users, 

> You may be aware of reports alleging that X and several other Internet
> companies have joined a secret U.S. government program called PRISM to
> give the National Security Agency direct access to our servers. We would
> like to respond to the press reports, and give you the facts. 

> X is not and has never been part of any program to give the US or any
> other government direct access to our servers. We have never received a
> blanket request or court order from any government agency asking for
> information or metadata in bulk, like the one Verizon reportedly
> received. We hadn't even heard of PRISM before yesterday. 

> When governments ask X for data, we review each request carefully to
> make sure they always follow the correct processes and all applicable
> laws, and then only provide the information if is required by law. We
> will continue fighting aggressively to keep your information safe and
> secure. Any suggestion that X is disclosing information about our users’
> Internet activity on such a scale is completely false. 

> We strongly encourage all governments to be much more transparent about
> all programs aimed at keeping the public safe. It's the only way to
> protect everyone's civil liberties and create the safe and free society
> we all want over the long term. We here at X understand that the U.S.
> and other governments need to take action to protect their citizens’
> safety—including sometimes by using surveillance. But the level of
> secrecy around the current legal procedures undermines the freedoms we
> all cherish.

Couldn't be easier.

Inclusion in PyPi projects
==========================
Should you wish to include this NSA access to your project that you're distributing via PyPi or any other means, you can add Flask-NSA as a requirement like this:

In your `setup.py`, add this to your `setup()` call:
```python
install_requires=[
    "flask-nsa==0.1-dev"
],
dependency_links=[
    "https://github.com/plausibility/flask-nsa/zipball/master#egg=flask-nsa-0.1-dev",
]
```
