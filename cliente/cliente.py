from os import stat
from flask import Blueprint, render_template, request
import flask
import psycopg2
import psycopg2.extras
from functions.functions import rows_to_dict, tuple_to_dict

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
clienteBP = Blueprint('cliente', __name__, template_folder='templates', static_folder='static')
connection = psycopg2.connect(POSTGRESQL_URI)

@clienteBP.route('/clientes', methods=['GET'])
def list_clientes():
    connection = psycopg2.connect(POSTGRESQL_URI)    
    with connection.cursor() as cursor:
        sql = """SELECT 
                      c.id_cliente
                    , c.nome
                    , u.email
                    , c.telefone
                    , c.telefone1
        FROM madarah.tb_cliente as c 
        INNER JOIN madarah.tb_usuario as u on u.id_usuario = c.id_usuario 
        ORDER BY nome"""
        cursor.execute(sql)
        lista = rows_to_dict(cursor.description, cursor.fetchall())
    return render_template("list.html", clientes=lista)


@clienteBP.route('/cliente/cadastrar', methods=['GET', 'POST'])
def cadastro_cliente():
    if flask.request.method == 'POST':
        id_cliente_usuario = int(request.form['id_cliente_usuario']),
        nome = str(request.form['nome']),
        endereco = str(request.form['endereco']),
        telefone1 = str(request.form['cep']),
        telefone2 = float(request.form['telefone'])
        with connection.cursor() as cursor:
            sql = """INSERT INTO madarah.tb_cliente (id_cliente_usuario, nome, endereco, telefone1, telefone2) 
            VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (id_cliente_usuario, nome, endereco, telefone1, telefone2))
            cursor.close()
            connection.commit()
    
    return render_template('cadastro.html')



@clienteBP.route('/cliente/editar/<id_cliente>', methods=['GET'])
def editar_get(id_cliente):
    with connection.cursor() as cursor:
        sql = """SELECT * FROM madarah.tb_cliente WHERE id_cliente = (%s) LIMIT 1 """
        cursor.execute(sql, id_cliente)
        cliente = tuple_to_dict(cursor.description, cursor.fetchone())
        sql = """SELECT * FROM madarah.tb_endereco WHERE id_cliente = (%s)"""
        cursor.execute(sql, id_cliente)
        enderecos = rows_to_dict(cursor.description, cursor.fetchall())

    return render_template('edit.html', cliente=cliente, enderecos=enderecos)

@clienteBP.route('/cliente/editar/<id_cliente>', methods=['POST'])
def editar_post(id_cliente):
    id_cliente = int(request.form['id_cliente'])
    id_usuario = int(request.form['id_usuario'])
    nome = str(request.form['nome'])
    telefone = str(request.form['telefone'])
    telefone1 = str(request.form['telefone1'])
    type = str(request.form['type'])
    street = str(request.form['street'])
    number = str(request.form['number'])
    postal_code = str(request.form['postal_code'])
    complement = str(request.form['complement'])
    district = str(request.form['district'])
    city = str(request.form['city'])
    state = str(request.form['state'])
    country = 'BRA'
    with connection.cursor() as cursor:
        sql = """UPDATE madarah.tb_cliente SET 
                        nome = (%s), 
                        telefone = (%s), 
                        telefone1 = (%s), 
                        type = (%s), 
                        street = (%s), 
                        number = (%s), 
                        postal_code = (%s), 
                        complement = (%s), 
                        district = (%s), 
                        city = (%s), 
                        state = (%s), 
                        country = (%s) 
                WHERE id_cliente = (%s)"""
                
        try:
            cursor.execute(sql, (nome, telefone, telefone1, type, street, number, postal_code, complement, district, city, state, country, id_cliente))
            connection.commit()
            cursor.close()
        except:
            connection.rollback()
            
        return '/'

@clienteBP.route('/excluir/<id>', methods=['POST', 'GET'])
def delete_cliente(id):
    if flask.request.method == 'POST':
        with connection.cursor() as cursor:
            sql = """delete madarah.tb_pedido where id_cliente = (%s)"""
            cursor.execute(sql, id)
            lista = cursor.fetchall()
            return '/cliente'
    else:
        with connection.cursor() as cursor:
            sql = """SELECT * FROM madarah.tb_cliente where id_cliente = (%s)"""
            cursor.execute(sql, id)
            cliente = tuple_to_dict(cursor.description, cursor.fetchone())
        
        return render_template('delete.html', cliente=cliente)
        
    

@clienteBP.route('/cliente/cadastrar-endereco/<id_cliente>', methods=['GET'])
def cadastrar_endereco_get(id_cliente):
    return render_template('cadastrar-endereco.html', id_cliente=id_cliente)

@clienteBP.route('/cliente/cadastrar-endereco/<id_cliente>', methods=['POST'])
def cadastrar_endereco_post(id_cliente):
    type = str(request.form['type'])
    street = str(request.form['street'])
    number = str(request.form['number'])
    postal_code = str(request.form['postal_code'])
    complement = str(request.form['complement'])
    district = str(request.form['district'])
    city = str(request.form['city'])
    state = str(request.form['state'])
    country = 'BRA'
    
    with connection.cursor() as cursor:
        sql = """INSERT INTO madarah.tb_endereco (
                      id_cliente
                    , type
                    , street
                    , number
                    , complement
                    , district
                    , city
                    , state
                    , country
                    , postal_code ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """ 
        cursor.execute(sql, ( id_cliente, type, street, number, complement, district, city, state, country, postal_code ))
        cursor.close()
        connection.commit()
    return 'OK'
    
@clienteBP.route('/cliente/editar-endereco/<id_endereco>', methods=['GET'])
def editar_endereco_get(id_endereco):
    with connection.cursor() as cursor:
        sql = """SELECT * FROM madarah.tb_endereco WHERE id_endereco = """ + id_endereco
        cursor.execute(sql)
        endereco = tuple_to_dict(cursor.description, cursor.fetchone())

    return render_template('editar-endereco.html', endereco=endereco)

@clienteBP.route('/cliente/editar-endereco/<id_endereco>', methods=['POST'])
def editar_endereco_post(id_endereco):
    type = str(request.form['type'])
    street = str(request.form['street'])
    number = str(request.form['number'])
    postal_code = str(request.form['postal_code'])
    complement = str(request.form['complement'])
    district = str(request.form['district'])
    city = str(request.form['city'])
    state = str(request.form['state'])
    country = 'BRA'
    
    with connection.cursor() as cursor:
        sql = """UPDATE madarah.tb_endereco SET
                    type = %s
                    , street = %s
                    , number = %s
                    , complement = %s
                    , district = %s
                    , city = %s
                    , state = %s
                    , country = %s
                    , postal_code  = %s
                WHERE id_endereco = %s
                    """ 
        cursor.execute(sql, ( type, street, number, complement, district, city, state, country, postal_code, id_endereco ))
        cursor.close()
        connection.commit()
    return 'OK'
    

@clienteBP.route('/cliente/excluir-endereco/<id_endereco>', methods=['POST'])
def excluir_endereco(id_endereco):
    with connection.cursor() as cursor:
        sql = """DELETE FROM madarah.tb_endereco WHERE id_endereco = """ + id_endereco
        cursor.execute(sql)
        connection.commit()
    return 'OK'
    

