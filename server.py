import json
from os import environ as env
from config import Config
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from flask_flatpages import FlatPages

ENV_FILE = find_dotenv() # finds the env and loads credentials!! Woohoo
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)

app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_ROOT'] = 'blog_posts'

app.secret_key = env.get("APP_SECRET_KEY") # configuring flask for my app via the generated key.

flatpages = FlatPages(app)

oauth = OAuth(app)

@app.route("/")
def home():

    posts = flatpages

    return render_template("home.html", posts=posts)

@app.route("/blog/<path:path>/")
def blog_post(path):
    post = flatpages.get_or_404(path)
    return render_template("blog_post.html", post=post)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000), debug=True)
