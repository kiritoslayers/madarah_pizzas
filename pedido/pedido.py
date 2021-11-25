from flask import Blueprint, render_template, request, session
import flask
import psycopg2
import psycopg2.extras

from functions.functions import row_to_dict, rows_to_dict, tuple_to_dict

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
pedidoBP = Blueprint('pedido', __name__, template_folder='templates', static_folder='static')
connection = psycopg2.connect(POSTGRESQL_URI)

@pedidoBP.route('/pedidos', methods=['GET'])
def listar():
    authenticate =  session if 'google_id' in session else False
    cliente = session['cliente'] or False
    usuario = session['usuario'] or False
    with connection.cursor() as cursor:
        sql = """SELECT 
              p.id_pedido
            ,  p.codigo_de_compra as codigo
            ,  p.total
            ,  p.date
            ,  p.status
            ,  u.nome
            ,  u.email
            ,  c.telefone
            ,  c.telefone1
            ,  c.type
            ,  c.street
            ,  c.number
            ,  c.complement
            ,  c.district
            ,  c.postal_code
            ,  c.city
            ,  c.state
            ,  c.country
        FROM madarah.tb_pedido as p
        INNER JOIN madarah.tb_cliente as c ON c.id_cliente = p.id_cliente
        INNER JOIN madarah.tb_usuario as u ON u.id_usuario = c.id_usuario
        ORDER BY date"""
        cursor.execute(sql)
        lista = rows_to_dict(cursor.description, cursor.fetchall())
        
    return render_template("listar.html", pedidos=lista, auth=authenticate, cliente=cliente, usuario=usuario)

@pedidoBP.route('/meus-pedidos', methods=['GET'])
def list_meus_pedidos():
    authenticate =  session if 'google_id' in session else False
    cliente = session['cliente'] or False;
    usuario = session['usuario'] or False;
    with connection.cursor() as cursor:
        sql = """SELECT 
              p.id_pedido
            ,  p.codigo_de_compra as codigo
            ,  p.total
            ,  p.date
            ,  p.status
            ,  u.nome
            ,  u.email
            ,  c.telefone
            ,  c.telefone1
            ,  c.type
            ,  c.street
            ,  c.number
            ,  c.complement
            ,  c.district
            ,  c.postal_code
            ,  c.city
            ,  c.state
            ,  c.country
        FROM madarah.tb_pedido as p
        INNER JOIN madarah.tb_cliente as c ON c.id_cliente = p.id_cliente
        INNER JOIN madarah.tb_usuario as u ON u.id_usuario = c.id_usuario
        WHERE p.id_cliente = %s ORDER BY date"""
        cursor.execute(sql, str(cliente['id_cliente']))
        lista = rows_to_dict(cursor.description, cursor.fetchall())
        
        
    return render_template("meus-pedidos.html", pedidos=lista, auth=authenticate, cliente=cliente, usuario=usuario)
    
@pedidoBP.route('/pedido/confirmar-endereco', methods=['GET'])
def confirmar_endereco_get():
    cliente = session['cliente']
    with connection.cursor() as cursor: 
        sql = """SELECT * FROM madarah.tb_endereco WHERE id_cliente = (%s) AND ativo = true"""
        cursor.execute(sql, str(cliente['id_cliente']))
        enderecos = rows_to_dict(cursor.description, cursor.fetchall())

    return render_template('confirmar-endereco.html', cliente=cliente, enderecos=enderecos)


@pedidoBP.route('/pedido/confirmar-endereco', methods=['POST'])
def confirmar_endereco_post():
    cliente = session['cliente']
    type = str(request.form['type'])
    street = str(request.form['street'])
    number = str(request.form['number'])
    postal_code = str(request.form['postal_code'])
    complement = str(request.form['complement'])
    district = str(request.form['district'])
    city = str(request.form['city'])
    state = str(request.form['state'])
    country = 'BRA'
    enderecoPadrao = True if str(request.form['enderecoPadrao']) == 'true' else False

    


    return 'OK'


@pedidoBP.route('/pedido/pedido-finalizado/<id>')
def pedido_finalizado(id):
    authenticate =  session if 'google_id' in session else False
    with connection.cursor() as cursor: 
        cliente = False
        user = False
        if authenticate:
            sql = """SELECT * FROM madarah.tb_usuario WHERE google_id = '""" + authenticate['google_id'] + """' LIMIT 1"""
            cursor.execute(sql)
            user = tuple_to_dict(cursor.description, cursor.fetchone())

            sql = """SELECT * FROM madarah.tb_cliente WHERE id_usuario = """ + str(user['id_usuario']) + """ LIMIT 1"""
            cursor.execute(sql)
            cliente = tuple_to_dict(cursor.description, cursor.fetchone())

            sql = """SELECT * 
                    FROM madarah.tb_pedido as p
                    WHERE id = %s LIMIT 1"""
            cursor.execute(sql)
            pedido = tuple_to_dict(cursor.description, cursor.fetchone())

        session['usuario'] = user
        session['cliente'] = cliente

    return render_template('pedido-finalizado.html', auth=authenticate, cliente=cliente, usuario=user)


@pedidoBP.route('/pedidos/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if flask.request.method == 'POST':
        connection = psycopg2.connect(POSTGRESQL_URI)
        id_cliente_usuario = int(request.form['id_cliente_usuario']),
        nome = str(request.form['nome']),
        endereco = str(request.form['endereco']),
        telefone1 = str(request.form['cep']),
        telefone2 = float(request.form['telefone'])
        status = float(request.form['status'])
        with connection.cursor() as cursor:
            sql = """insert into madarah.tb_pedido (id_cliente_usuario, nome, endereco, telefone1, telefone2, status) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (id_cliente_usuario, nome, endereco, telefone1, telefone2, status))
            cursor.close()
            connection.commit()
    
    return render_template('cadastro.html')



@pedidoBP.route('/pedidos/editar', methods=['POST', 'GET'])
def editar():
    if flask.request.method == 'POST':
        id_cliente_usuario = int(request.form['id_cliente_usuario']),
        nome = str(request.form['nome']),
        endereco = str(request.form['endereco']),
        telefone1 = str(request.form['cep']),
        telefone2 = float(request.form['telefone'])
        status = float(request.form['status'])
        with connection.cursor() as cursor:
            sql = """update madarah.tb_pedido SET nome = (%s), endereco = (%s), telefone1 = (%s), telefone2 = (%s), status = (%s) WHERE id_cliente_usuario = (%s)"""
            cursor.execute(sql, ( nome, endereco, telefone1, telefone2, status, id_cliente_usuario))
            cursor.close()
            connection.commit()
    return render_template('edicao.html')



@pedidoBP.route('/pedidos/excluir/<int:id>', methods=['POST', 'GET'])
def excluir(id):
    with connection.cursor() as cursor:
        sql = """delete madarah.tb_pedido where id_pedido = (%s)"""
        cursor.execute(sql, id)
        lista = cursor.fetchall()
    return render_template('delete.html')

@pedidoBP.route('/pedidos/status/<int:id>', methods=['POST'])
def status(id):
    status = str(request.form['status'])
    with connection.cursor() as cursor:
        sql = """UPDATE madarah.tb_pedido SET status = (%s) where id_pedido = (%s) returning * """
        cursor.execute(sql, (status, str(id)))
        connection.commit()
    return 'OK'



@pedidoBP.route('/pedidos/cadastrar-endereco/<id_cliente>', methods=['GET'])
def cadastrar_endereco_get(id_cliente):
    return render_template('cadastrar-endereco.html', id_cliente=id_cliente)

@pedidoBP.route('/pedidos/cadastrar-endereco/<id_cliente>', methods=['POST'])
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
    
@pedidoBP.route('/pedidos/editar-endereco/<id_endereco>', methods=['GET'])
def editar_endereco_get(id_endereco):
    with connection.cursor() as cursor:
        sql = """SELECT * FROM madarah.tb_endereco WHERE id_endereco = """ + id_endereco
        cursor.execute(sql)
        endereco = tuple_to_dict(cursor.description, cursor.fetchone())

    return render_template('editar-endereco.html', endereco=endereco)

@pedidoBP.route('/pedidos/editar-endereco/<id_endereco>', methods=['POST'])
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
    

@pedidoBP.route('/pedidos/excluir-endereco/<id_endereco>', methods=['POST'])
def excluir_endereco(id_endereco):
    with connection.cursor() as cursor:
        sql = """UPDATE madarah.tb_endereco SET
                    ativo = false
                WHERE id_endereco = """ + id_endereco
        cursor.execute(sql)
        cursor.close()
        connection.commit()
        
    return 'OK'