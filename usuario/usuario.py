from functions.functions import rows_to_dict, tuple_to_dict
from flask import Blueprint, render_template, request, redirect
import flask
import psycopg2
import psycopg2.extras
from functions import *
# import crypt

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
userBP = Blueprint('usuario', __name__, template_folder='templates', static_folder='static')

@userBP.route('/account/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # oi = crypt.crypt(email)
        return '/'
    else:
        return render_template('login.html')

    