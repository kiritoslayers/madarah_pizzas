from os import stat
from flask import Blueprint, render_template, request, session
import flask
import psycopg2
import psycopg2.extras
from functions.functions import rows_to_dict, tuple_to_dict

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
perfilBP = Blueprint('perfil', __name__, template_folder='templates', static_folder='static')
connection = psycopg2.connect(POSTGRESQL_URI)

@perfilBP.route('/profile', methods=['GET'])
def perfil():
    cliente = session['cliente']
    with connection.cursor() as cursor:
        sql = """SELECT * FROM madarah.tb_endereco WHERE id_cliente = (%s) AND ativo = true"""
        cursor.execute(sql, str(cliente['id_cliente']))
        enderecos = rows_to_dict(cursor.description, cursor.fetchall())

    return render_template('profile.html', cliente=cliente, enderecos=enderecos)

@perfilBP.route('/profile/editar/', methods=['POST'])
def editar_post():
    id_cliente = int(request.form['id_cliente'])
    nome = str(request.form['nome'])
    telefone = str(request.form['telefone'])
    telefone1 = str(request.form['telefone1'])
   
    with connection.cursor() as cursor:
        sql = """UPDATE madarah.tb_cliente SET 
                        nome = (%s), 
                        telefone = (%s), 
                        telefone1 = (%s)
                WHERE id_cliente = (%s)"""
        try:
            cursor.execute(sql, (nome, telefone, telefone1, id_cliente))
            connection.commit()
            cursor.close()
        except:
            connection.rollback()
            
        return '/'

@perfilBP.route('/profile/cadastrar-endereco', methods=['GET'])
def cadastrar_endereco_get():
    id_cliente = session['cliente']['id_cliente']
    return render_template('cadastrar_endereco.html', id_cliente=id_cliente)

@perfilBP.route('/profile/cadastrar-endereco/<id_cliente>', methods=['POST'])
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
                    , postal_code
                    , ativo ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, true) """ 
        cursor.execute(sql, ( id_cliente, type, street, number, complement, district, city, state, country, postal_code ))
        cursor.close()
        connection.commit()
    return 'OK'
    
@perfilBP.route('/profile/editar-endereco/<id_endereco>', methods=['GET'])
def editar_endereco_get(id_endereco):
    with connection.cursor() as cursor:
        sql = """SELECT * FROM madarah.tb_endereco WHERE id_endereco = """ + id_endereco
        cursor.execute(sql)
        endereco = tuple_to_dict(cursor.description, cursor.fetchone())
    return render_template('editar_endereco.html', endereco=endereco)

@perfilBP.route('/profile/editar-endereco/<id_endereco>', methods=['POST'])
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

@perfilBP.route('/profile/excluir-endereco/<id_endereco>', methods=['POST'])
def excluir_endereco(id_endereco):
    with connection.cursor() as cursor:
        sql = """UPDATE madarah.tb_endereco SET
                    ativo = false
                WHERE id_endereco = """ + id_endereco
        cursor.execute(sql)
        cursor.close()
        connection.commit()
        
    return 'OK'
    

