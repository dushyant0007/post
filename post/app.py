
import os
import sqlite3
import pathlib
import requests
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests


app = Flask("post")  # naming our application
# it is necessary to set a password when dealing with OAuth 2.0
app.secret_key = "mykey"
# this is to set our environment to https because OAuth 2.0 only supports https environments
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# enter your client id you got from Google console
GOOGLE_CLIENT_ID = "1053079030385-90cls831re1tbo1p6ev9eecnfukg6lod.apps.googleusercontent.com"
# set the path to where the .json file you got Google console is
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file( client_secrets_file=client_secrets_file,scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email","openid"], redirect_uri="https://dushyant0007-solid-cod-rp7q9w7qjwvhxjpx-5000.preview.app.github.dev/callback")


# a function to check if the user is authorized or not
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  # authorization required
            return abort(401)
        else:
            return function()
    return wrapper


@app.route("/login")  # the page where the user can login
def login():
    # asking the flow class for the authorization (login) url
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


# this is the page that will handle the callback process meaning process after the authorization
@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # defing the results to show on the page
    # session['hd'] = id_info('hd') #hd -> whatever after @ ex -> abc@this.is.hd
    session['hd'] = ''
    try:
        session['hd'] = id_info['hd']
    finally:
        session["google_id"] = id_info.get("sub")
        session['email'] = id_info.get('email')
        session["name"] = id_info.get("name")
        session['photo'] = id_info.get('picture')
        # the final page where the authorized users will end up
        print(id_info)
        print('--------------,.,.,.,.,,->')
        print(session['hd'])
        if session['hd'] == 'skit.ac.in':
            return redirect("/home")
        else:
            return redirect('/')


@app.route("/logout")  # the logout page and function
def logout():
    session.clear()
    return redirect("/")


@app.route("/")  # the home page where the login button will be located
def index():
    return render_template('index.html')


# the page where only the authorized users can go to
@app.route("/home")
@login_is_required
def protected_area():
    with sqlite3.connect("database.db") as db:
        x = db.execute("select google_id from user where google_id=(?)",
                       (session['google_id'],)).fetchone()
        print("The value of x")
        print(x)
        if x == None:
            db.execute("insert into user (google_id,name,email,photo) values (?,?,?,?) ",
                       (session['google_id'], session['name'], session["email"], session["photo"]))
            db.commit()
    return render_template('home.html')


@app.route("/post", methods=['POST'])
def post():
    if request.form.get('post') == "":
        return redirect("/home")
    with sqlite3.connect("database.db") as db:
        post = request.form.get('post')
        db.execute("insert into post (google_id,post) values (?,?) ",
                   (session['google_id'], post))
        db.commit()
    return redirect('/home')


@app.route("/all_post")
def all_post():
    if 'google_id' not in session:
        return redirect('/')
    with sqlite3.connect("database.db") as db:
        p = db.execute(
            'select * from (user join post on user.google_id=post.google_id)').fetchall()
        print(p)
        return render_template('all_post.html', all_post=p)


if __name__ == "__main__":  # and the final closing function
    app.run(debug=True)
