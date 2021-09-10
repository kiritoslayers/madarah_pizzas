from functions.functions import rows_to_dict, tuple_to_dict
from flask import Blueprint, render_template, request
import flask
import psycopg2
import psycopg2.extras
from functions import *

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
pizzaBP = Blueprint('pizza', __name__, template_folder='templates', static_folder='static')

@pizzaBP.route('/pizzas', methods=['GET'])
def list():
    connection = psycopg2.connect(POSTGRESQL_URI)
    with connection.cursor() as cursor:
        sql = """select * from madarah.tb_pizza order by sabor"""
        cursor.execute(sql)
        lista = rows_to_dict(cursor.description, cursor.fetchall())
    return render_template("list.html", pizzas=lista)



@pizzaBP.route('/pizza/cadastro', methods=['GET', 'POST'])
def cadastro_pizza():
    if flask.request.method == 'POST':
        sabor = str(request.form['sabor']),
        descricao = str(request.form['descricao']),
        valor = request.form['valor'].replace('.', ',').replace(',', '.')
        valor = float(valor)
        url_foto = str(request.form['url_foto'])
        connection = psycopg2.connect(POSTGRESQL_URI)
        with connection.cursor() as cursor:
            sql = """insert into madarah.tb_pizza (sabor, descricao, valor, url_foto) VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (sabor, descricao, valor, url_foto))
            connection.commit()
            cursor.close()
        return '/pizzas'

    return render_template('cadastro.html')


@pizzaBP.route('/pizza/edicao/<id>', methods=['GET', 'POST'])
def edicao_pizza(id):
    connection = psycopg2.connect(POSTGRESQL_URI)
    if flask.request.method == 'POST':
        id_pizza = int(request.form['id_pizza'])
        sabor = str(request.form['sabor']),
        descricao = str(request.form['descricao']),
        valor = request.form['valor'].replace('.', ',').replace(',', '.')
        valor = float(valor)
        url_foto = str(request.form['url_foto'])
        with connection.cursor() as cursor:
            sql = """update madarah.tb_pizza SET sabor = (%s), descricao = (%s), valor = (%s), url_foto = (%s) WHERE id_pizza = (%s)"""
            cursor.execute(sql, (sabor, descricao, valor, url_foto, id_pizza))
            connection.commit()
            cursor.close()
        return '/pizzas'
    else:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM madarah.tb_pizza WHERE id_pizza = (%s)"""
            cursor.execute(sql, (id))
            pizza = tuple_to_dict(cursor.description, cursor.fetchall())
        return render_template('edicao.html', pizza=pizza)
    



@pizzaBP.route('/pizza/delete/<id>', methods=['GET', 'POST'])
def delete_pizza(id):
    connection = psycopg2.connect(POSTGRESQL_URI)
    if flask.request.method == 'POST':
        with connection.cursor() as cursor:
            sql = """delete from madarah.tb_pizza where id_pizza = (%s)"""
            cursor.execute(sql, (id))
            connection.commit()
            cursor.close()
        return '/pizzas'
    else:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM madarah.tb_pizza WHERE id_pizza = (%s)"""
            cursor.execute(sql, (id))
            pizza = tuple_to_dict(cursor.description, cursor.fetchall())
        return render_template('delete.html', pizza=pizza)
