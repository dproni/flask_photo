from flask import Flask, flash, redirect, url_for
from flask import request
from flask import render_template
from tools import getFromMongo
from flask.ext.pymongo import PyMongo

from flask.ext.login import (LoginManager, current_user, login_required,
                             login_user, logout_user, UserMixin, AnonymousUser,
                             confirm_login, fresh_login_required)

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active


class Anonymous(AnonymousUser):
    name = u"Anonymous"


USERS = {
    1: User(u"Notch", 1),
    2: User(u"Steve", 2),
    3: User(u"Creeper", 3, False),
    }

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())


app = Flask(__name__)

SECRET_KEY = "yeah, not actually a secret"
DEBUG = True

app.config.from_object(__name__)

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))

login_manager.setup_app(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        if username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")


@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/test/', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        mongo.db.content.update({'page': 1}, {"$set": {'content': request.values['content']}})
        return '1'
    else:
        flash('You were successfully logged in')
        content = mongo.db.content.find_one({'page':1}) or {'content': ' '}
        return render_template('test.html', content=content['content'])

@app.route('/pic/', methods=['GET'])
def return_pic():
    return 'http://lworkshop.com/img/logo.png'

@app.route('/photographers/')
def photographers():
    photos = getFromMongo(base='photos', coll='albums', split=5)
    return render_template('photo.html', photos = photos)

@app.route('/decorators/')
def decorators():
    photos = getFromMongo(base='photos', coll='photos', split=5)
    return render_template('decor.html', photos = photos)

@app.route('/person/<int:id>/')
def person(id):
    photos  = getFromMongo(base='photos', coll='photos', split=5, search={'album': id})
    album   = getFromMongo(base='photos', coll='albums', search={'album': id})
    return render_template('person.html',
                           photos       = photos,
                           title        = album[0]['title'],
                           description  = album[0]['description']
    )

if __name__ == '__main__':
    mongo = PyMongo(app)
    # Secret key needed to use sessions.
    app.secret_key = 'N4BUdSXUzHxNoO8g'
    app.debug = True
    app.run(host='192.168.0.103')
