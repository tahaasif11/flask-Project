# save this as app.py
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/user/<user>')
def profile(user):
    return render_template('user.html', user=user)


@app.route('/about')
def about():
    return render_template('weather_api.html')


@app.route('/contact/<name>')
def contact(name):
    return f"<h1>Hello {name}!</h1>"


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error_404.html")


@app.errorhandler(500)
def server_error(error):
    return render_template("error_500.html")


app.run(debug=True)
