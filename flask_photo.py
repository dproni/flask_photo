from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/photographers/')
def photographers():
    return render_template('photo.html')

@app.route('/decorators/')
def decorators():
    return render_template('decor.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
