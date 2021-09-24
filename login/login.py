from flask import Blueprint, render_template # , request
import flask
import psycopg2
import psycopg2.extras

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
loginBP = Blueprint('login', __name__, template_folder='template', static_folder='static')

def connect():
    connection = psycopg2.connect(POSTGRESQL_URI)
    return connection


@loginBP.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        email = flask.request.form['email']
        senha = flask.request.form['senha']
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM accounts WHERE email = %s AND senha = %s', (email, senha))
            cursor.fetchone()
            cursor.close()
        return '/login'
        

    return(render_template('login.html'))
    