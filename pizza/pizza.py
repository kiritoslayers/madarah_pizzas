from flask import Blueprint, render_template, request
import flask
import psycopg2
import psycopg2.extras


POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
pizzaBP = Blueprint('pizza', __name__, template_folder='templates', static_folder='static')


@pizzaBP.route('/cardapio', methods=['GET'])
def home_pizza():
    return render_template('cardapio.html')


@pizzaBP.route('/cadastro_pizza', methods=['GET', 'POST'])
def cadastro_pizza():
    if flask.request.method == 'POST':
        sabor = str(request.form['sabor']),
        descricao = str(request.form['descricao']),
        valor = float(request.form['valor'])
        url_foto = str(request.form['url_foto'])
        connection = psycopg2.connect(POSTGRESQL_URI)
        with connection.cursor() as cursor:
            sql = """insert into madarah.tb_pizza (sabor, descricao, valor, url_foto) VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (sabor, descricao, valor, url_foto))
            cursor.close()
            connection.commit()
    return render_template('cadastro.html')



@pizzaBP.route('/editar_pizza', methods=['GET', 'POST'])
def edicao_pizza():
    if flask.request.method == 'POST':
        id = int(request.form['id']),
        sabor = str(request.form['sabor']),
        descricao = str(request.form['descricao']),
        valor = float(request.form['valor'])
        url_foto = str(request.form['url_foto'])
        connection = psycopg2.connect(POSTGRESQL_URI)
        with connection.cursor as cursor:
            sql = """update madarah.tb_pizza SET sabor = (%s), descricao = (%s), valor = (%s), url_foto = (%s) WHERE id_pizza = (%s)"""
            cursor.execute(sql, (sabor, descricao, valor, url_foto, id))
            cursor.close()
            connection.commit()
    return render_template('edicao.html')
