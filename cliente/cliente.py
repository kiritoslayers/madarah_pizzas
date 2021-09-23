from datetime import date
from flask import Blueprint, render_template, request
import flask
import psycopg2
import psycopg2.extras


POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
clienteBP = Blueprint('cliente', __name__, template_folder='templates', static_folder='static')



@clienteBP.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if flask.request.method == 'POST':
        id_cliente_usuario = int(request.form['id_cliente_usuario']),
        nome = str(request.form['nome']),
        endereco = str(request.form['endereco']),
        telefone1 = str(request.form['cep']),
        telefone2 = float(request.form['telefone'])
        connection = psycopg2.connect(POSTGRESQL_URI)
        with connection.cursor() as cursor:
            sql = """insert into madarah.tb_cliente (id_cliente_usuario, nome, endereco, telefone1, telefone2) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (id_cliente_usuario, nome, endereco, telefone1, telefone2))
            cursor.close()
            connection.commit()
    
    return render_template('cadastro_cliente.html')



@clienteBP.route('/editar_cliente', methods=['POST', 'GET'])
def edicao_cliente(id_cliente_usuario):
    if flask.request.method == 'POST':
        id_cliente_usuario = int(request.form['id_cliente_usuario']),
        nome = str(request.form['nome']),
        endereco = str(request.form['endereco']),
        telefone1 = str(request.form['cep']),
        telefone2 = float(request.form['telefone'])
        connection = psycopg2.connect(POSTGRESQL_URI)
        with connection.cursor() as cursor:
            sql = """update madarah.tb_cliente SET nome = (%s), endereco = (%s), telefone1 = (%s), telefone2 = (%s) WHERE id_cliente_usuario = (%s)"""
            cursor.execute(sql, ( nome, endereco, telefone1, telefone2, id_cliente_usuario))
            cursor.close()
            connection.commit()
    return render_template('edit_cliente.html')



@clienteBP.route('/clientes', methods=['GET'])
def list_clientes():
    connection = psycopg2.connect(POSTGRESQL_URI)    
    with connection.cursor() as cursor:
        sql = """select * from madarah.tb_cliente order by nome"""
        cursor.execute(sql)
        lista = cursor.fetchall()
    return render_template("list_clientes.html", clientes=lista)



@clienteBP.route('/delete_cliente/<int:cpf>', methods=['POST', 'GET'])
def delete_cliente(cpf):
    connection = psycopg2.connect(POSTGRESQL_URI)    
    with connection.cursor() as cursor:
        sql = """delete madarah.tb_pedido where cpf = (%s)"""
        cursor.execute(sql, cpf)
        lista = cursor.fetchall()
    return render_template('delete_cliente.html')
        
    

