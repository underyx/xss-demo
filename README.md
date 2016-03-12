XSS Demo
========

Example application and scripts to demonstrate some XSS vulnerabilities.

The vulnerable Pyramid application (a blog where the administrator can post new
entries and were anyone can add comments) can be found in the app/
subdirectory.


Setup
-----

This setup was tested on Ubuntu 15.10 and it should work out of the box on any
recent Debian based Linux distribution (with Python 3). Setting it up on other
Operating Systems should not be a problem but the instructions need to be
adapted.

**bcrypt** is used as a dependency. This requires **libffi-dev** to be
installed:

```bash
sudo apt-get install libffi-dev
```

To start the application clone the repository and setup a Python virtualenv:

```bash
mkdir xss-demo && cd xss-demo
git clone https://github.com/omarkohl/xss-demo.git
virtualenv -p python3 venv
source venv/bin/activate
pip install -U setuptools && pip install -U pip
cd xss-demo/app
pip install -r dev_requirements.txt
python setup.py develop
```

Now you can start the application:

```bash
pserve development.ini
```

and access it in your browser on http://localhost:6543


Running
-------

The application is a simple blog where the Administrator can publish new
blogposts and anyone can add comments to the blogs. There is a search function
that does nothing except show a XSS vulnerability.

Several blogposts and comments are setup on application startup out of the box.
The *database* (just in memory) is reset on every application start. The secret
key used to sign the cookies is also reset on every application start.

### Adding a comment

To add a comment simply click on any of the blogposts and use the form at the bottom. The comments will be displayed in chronological order.

### Logging in / Adding a post

To add a blogpost you need to log in with user *Administrator* and password *top-secret* .

Then click on the link in the menu and fill out the form.

### Searching

Currently the search is not linked anywhere but you can access it directly via URL: http://localhost:6543/search?q=myquery

Replace myquery with your searchterm. Nothing will be returned except an emtpy page displaying your searchterm. The purpose is to demonstrate a reflected XSS vulnerability (see below).


XSS
---

There are basically two types of XSS: Server and Client XSS. Each type can again be subdivided into Stored and Reflected XSS.

| **XSS**       | **Server**                | **Client**                |
| ------------- | ------------------------- | ------------------------- |
| **Stored**    | Stored Server XSS         | Stored Client XSS         |
| **Reflected** | Reflected Server XSS      | Reflected Client XSS      |

The *DOM based XSS* you might read about elsewhere is a subset of *Client XSS*.

See [OWASPs Types of XSS](https://www.owasp.org/index.php/Types_of_Cross-Site_Scripting) for more information.

This probject currently only shows examples of *Server XSS*. Feel free to
expand it to included *Client XSS* examples and send me a pull request.


Example of Reflected Server XSS
-------------------------------

The search functionality previously mentioned is an exampled of *Reflected
Server XSS*.

Reflected because the user data is simply reflected (returned) by the server and not stored. *Server XSS* because the flaw that allows for XSS to happen is on the server. The returned HTML contains code that is not properly encoded/escaped.

Open the following link:

```
http://localhost:6543/search?q=<script>alert(1)</script>
```

You should now see a JavaScript alert box with the number 1. If this is not displayed this is probably because your browser is too smart and prevents the attack. Open your Developer Console (Ctrl+Shift+I in Google Chrome) and look for a warning similar to this one:

> The XSS Auditor refused to execute a script in
> 'http://localhost:6543/search?q=%3Cscript%3Ealert(1)%3C/script%3E' because
> its source code was found within the request. The auditor was enabled as the
> server sent neither an 'X-XSS-Protection' nor 'Content-Security-Policy'
> header.

The big disadvantage of *Reflected XSS* (from the the attackers point of view)
is that you need to get the link to your victim. This required extra effort
(e.g. a phishing e-mail) and not as many users will be affected as with *Stored
XSS*. Plus it is comparatively easy for the browser to detect and block.
