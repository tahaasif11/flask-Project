
from flask import Flask, render_template, flash, g, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pymysql
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:Taha.Asif@localhost/flask'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = 'Taha.Asif'
# app.config['MYSQL_DB'] = 'flask'
app.config['SECRET_KEY'] ="12345"
# mysql = MySQL(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

def get_db_connection():
  if "connection" not in g or "cursor" not in g:
    g.connection, g.cursor = openDbconnection()
  return g.connection, g.cursor


def openDbconnection():
  try:
    connection = pymysql.connect(host='localhost', user='admin', passwd='Taha.Asif', db='flask')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor

  except Exception as e:
    print(e)
    raise

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit Form")


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    form = UserForm()
    connection, cursor = openDbconnection()
    cursor.execute("""
                SELECT * FROM users WHERE id= %s""",(id,))
    user = cursor.fetchone()
    if form.validate_on_submit():
        data = (form.name.data, form.email.data)
        cursor.execute("""
            UPDATE users SET username=%s, email=%s WHERE id=%s
        """, (form.name.data,form.email.data,id))
        connection.commit()
        flash("Successfully created")
        return redirect(url_for('profile', user=form.name.data))
    return render_template('user_edit.html', form=form,user=user)


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


@app.route('/register', methods=['GET','POST'])
def register():
    name = None
    form = UserForm()
    connection, cursor = openDbconnection()
    cursor.execute("""
                SELECT * FROM users""")
    users = cursor.fetchall()
    if form.validate_on_submit():
        # cursor = mysql.connection.cursor()
        
        data = (form.name.data, form.email.data)
        cursor.execute("""
                INSERT INTO users
                (username,email)
                VALUES (%s,%s)""", data)
       
        connection.commit()
        # mysql.connection.commit()
        name = form.name.data
        form.name.data = ''
        flash("Successfully created")
    return render_template('UserForm.html',form=form,name=name,users=users)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error_404.html")


@app.errorhandler(500)
def server_error(error):
    return render_template("error_500.html")


app.run(debug=True)
