import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import os
from config import Config
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from flask_flatpages import FlatPages

ENV_FILE = find_dotenv() # finds the env and loads credentials!! Woohoo
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = env.get("APP_SECRET_KEY") # configuring flask for my app via the generated key.

flatpages = FlatPages(app)

oauth = OAuth(app)

oauth.register( # Configure OAuth
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET","POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session['user'] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/tag/<string:tag>")
def tag(tag):
    posts = [p for p in flatpages if tag in p.meta.get('tags', [])]
    posts.sort(key=lambda item: item.meta['date'], reverse=True)
    return render_template("home.html", session=session.get('user'), posts=posts, tag=tag, pretty=json.dumps(session.get('user'), indent=4))

@app.route("/")
def home():
    posts = [p for p in flatpages]  
    posts.sort(key=lambda item: item.meta['date'], reverse=True)
    return render_template("home.html", session=session.get('user'), posts=posts, pretty=json.dumps(session.get('user'), indent=4))

def load_books():
    with open(os.path.join(app.root_path, 'static', 'books.json'), 'r') as f:
        books = json.load(f)
    return books

@app.route("/reading_list")
def reading_list():
    books_by_genre = load_books()
    return render_template("reading_list.html",books_by_genre=books_by_genre)

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000), debug=True)
