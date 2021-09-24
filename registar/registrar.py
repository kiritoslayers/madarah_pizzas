from typing import Coroutine
from flask import Blueprint, render_template
import flask
import psycopg2
import psycopg2.extras

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
registrarBP = Blueprint('registrar', __name__, template_folder='template', static_folder='static')

def connect():
    connection = psycopg2.connect(POSTGRESQL_URI)
    return connection


@registrarBP.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if flask.request.method == 'POST':
        mail = flask.request.form['email']
        senha = flask.request.form['senha']
        connection = connect()
        with connection.cursor() as cursor:
            sql = """insert into madarah.tb_usuario (email, senha) values (%s, %s)"""
            cursor.execute(sql,(mail, senha))
            connection.commit()
            cursor.close()
            return '/registrar'
    
    # DEVOLVER O TEMPLATE DO REGISTRAR AQUI
    return render_template()


    return # retornar o template de register