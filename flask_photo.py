from flask import Flask
from flask import render_template
from tools import getFromMongo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/photographers/')
def photographers():
    return render_template('photo.html')

@app.route('/decorators/')
def decorators():
    photos = getFromMongo(base='photos', coll='photos', split=5)
    return render_template('decor.html', photos = photos)


if __name__ == '__main__':
    app.debug = True
    app.run()
