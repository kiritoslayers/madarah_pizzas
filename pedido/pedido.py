# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session, redirect
import flask
from flask.helpers import make_response
import psycopg2
from functions.functions import row_to_dict, rows_to_dict, tuple_to_dict
import psycopg2.extras
import os
from pagseguro import PagSeguro
import random
from datetime import datetime
import requests

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
pedidoBP = Blueprint('pedido', __name__, template_folder='templates', static_folder='static')
connection = psycopg2.connect(POSTGRESQL_URI)

config = {'sandbox': True}

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
        FROM madarah.tb_pedido as p
        INNER JOIN madarah.tb_cliente as c ON c.id_cliente = p.id_cliente
        INNER JOIN madarah.tb_usuario as u ON u.id_usuario = c.id_usuario
        ORDER BY date"""
        cursor.execute(sql)
        lista = rows_to_dict(cursor.description, cursor.fetchall())
        
    return render_template("listar_pedidos.html", pedidos=lista, auth=authenticate, cliente=cliente, usuario=usuario)

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
    return render_template('create-endereco.html', id_cliente=id_cliente)

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

    return render_template('edit-endereco.html', endereco=endereco)

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


@pedidoBP.route('/pedidos/confirmar', methods=['GET'])
def confirmar_endereco_get():
    cliente = session['cliente']
    with connection.cursor() as cursor: 
        sql = """SELECT * FROM madarah.tb_endereco WHERE id_cliente = (%s) AND ativo = true"""
        cursor.execute(sql, str(cliente['id_cliente']))
        enderecos = rows_to_dict(cursor.description, cursor.fetchall()) 
        sql = """SELECT 
                c.id_item_carrinho
                , c.quantidade
                , c.id_cliente
                , p.sabor
                , p.descricao
                , p.valor
                , p.url_foto
                , p.weight
                , p.valor * c.quantidade AS total_item
                FROM 
                    madarah.tb_item_carrinho as c
                INNER JOIN madarah.tb_pizza as p ON p.id_pizza = c.id_pizza
                WHERE id_cliente = %s
            """
        cursor.execute(sql, str(cliente['id_cliente']))
        items_carrinho = rows_to_dict(cursor.description, cursor.fetchall()) 

    return render_template('confirmar.html', cliente=cliente, enderecos=enderecos, items_carrinho=items_carrinho)


@pedidoBP.route('/pedidos/finalizar/', methods=['GET'])
def finalizar():
    with connection.cursor() as cursor:
        cliente = session['cliente']
        usuario = session['usuario']
        # id_endereco = request.form['id_endereco']
        id_endereco = request.args['id_endereco']
        frete = 12.5
        if not(cliente) or not(usuario):
            return os.abort()

        if not(id_endereco):
            return os.abort()

        pg = PagSeguro(email="madarah.impacta@gmail.com", token="45B4AE1FB8684648B476ACA83627DA1D", data=None, config=config)
        pg.sender = {
            "name": str(usuario['nome']),
            "area_code": int(cliente['telefone1'].split(')')[0].replace('(', '')),
            "phone": int(cliente['telefone1'].split(')')[1].replace('.', '').replace('-', '')),
            "email": usuario['email'],
        }

        sql = '''SELECT * FROM madarah.tb_endereco WHERE id_endereco = ''' + id_endereco
        cursor.execute(sql)
        endereco = row_to_dict(cursor.description, cursor.fetchone())

        if not(endereco):
            return os.abort()

        # endereco de entrega
        pg.shipping = {
            "type": pg.NONE,
            "street": endereco['type'] + ' ' + endereco['street'],
            "number": endereco['number'],
            "complement": endereco['complement'],
            "district": endereco['district'],
            "postal_code": endereco['postal_code'],
            "city": endereco['city'],
            "state": endereco['state'],
            "country": endereco['country']
        }
    
        pg.reference_prefix = None # prefixo do codigo da compra
        pg.extra_amount = '{0:.2f}'.format(frete) # Valor extra (taxa de entrega - Float (positivo ou negativo)) 
    
        sql = """SELECT c.id_item_carrinho
                        , c.quantidade 
                        , p.id_pizza
                        , p.sabor
                        , p.descricao
                        , p.weight
                        , p.valor
                        , p.valor * c.quantidade AS total_item
                    FROM madarah.tb_item_carrinho as c
                    INNER JOIN madarah.tb_pizza as p ON p.id_pizza = c.id_pizza
                    WHERE c.id_cliente = %s LIMIT 1"""
        cursor.execute(sql, str(cliente['id_cliente']))
        lista = rows_to_dict(cursor.description, cursor.fetchall())

        total = 0
        pedido_pizza_rel = []
        for item in lista:
            pg.items.append(
                {
                    "id": item['id_item_carrinho'],
                    "description": item['sabor'] + ':   ' + item['descricao'],
                    "amount": float(item['valor']),
                    "quantity": item['quantidade'],
                    "weight": item['weight']
                }
            )
            total = total + item['total_item']
            pedido_pizza_rel.append({
                "quantidade": item['quantidade'],
                "id_pizza": item['id_pizza'],
                "id_pedido": None
            })

        codigo = str(random.random()).replace('.', '') # Codigo da compra
        pg.reference = codigo
        sql = """INSERT INTO madarah.tb_pedido (id_cliente, total, codigo_de_compra, date, id_endereco, frete, status) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s) returning *"""
        cursor.execute(sql, (str(cliente['id_cliente']), str(total), str(pg.reference), str(datetime.now()), str(id_endereco), str(frete), 'ProcessandoPagamento'))
        connection.commit()
        pedido = row_to_dict(cursor.description, cursor.fetchone())
        
        for item in lista:
            item['id_pedido'] = pedido['id_pedido']
            sql = """INSERT INTO madarah.tb_pedido_pizza_rel (id_pizza, id_pedido, quantidade) VALUES (%s, %s, %s) returning *"""
            cursor.execute(sql, (item['id_pizza'], item['id_pedido'], item['quantidade']))
            connection.commit()

        pg.redirect_url = "http://127.0.0.1:5000/pedido/pedido-finalizado/" + str(pedido['id_pedido']) # URL de redirecionamento ("http://meusite.com/obrigado")
        pg.redirect_url = 'www.google.com'

        response = pg.checkout()
        if(not(response.errors)):

            sql = """UPDATE madarah.tb_pedido SET codigo_de_compra = '""" + str(response.code) + """' WHERE id_pedido = """ + str(pedido['id_pedido'])
            cursor.execute(sql)
            connection.commit()


            sql = """DELETE FROM madarah.tb_item_carrinho WHERE id_cliente = """ + str(cliente['id_cliente'])
            cursor.execute(sql)
            connection.commit()

        return redirect(response.payment_url)



@pedidoBP.route('/pedidos/pedido-finalizado/<id>')
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


@pedidoBP.route('/pedidos/relatorio', methods=['GET'])
def relatorio():
    with connection.cursor() as cursor: 
        sql = """ SELECT p.id_pedido
                        , p.total
                        , p.codigo_de_compra
                        , p.date
                        , p.status
                        , p.frete
                        , c.nome
                        , c.telefone
                        , c.telefone1
                        , u.email
                        , e.type
                        , e.street
                        , e.number
                        , e.district
                        , e.postal_code
                        , e.city
                        , e.state
                    FROM madarah.tb_pedido as p
                    INNER JOIN  madarah.tb_cliente as c ON c.id_cliente = p.id_cliente
                    INNER JOIN  madarah.tb_endereco as e ON e.id_endereco = p.id_endereco
                    INNER JOIN  madarah.tb_usuario as u ON u.id_usuario = c.id_usuario
                    ORDER BY p.date
            """
        cursor.execute(sql)
        pedidos = rows_to_dict(cursor.description, cursor.fetchall())
        html = '''
            <h1> Relatório de pedidos </h1>
            <br>
        '''
        for item in pedidos:
            linha = """
                <p><strong>Código de compra</strong>: """ + item['codigo_de_compra'] + """ </p>
                <p><strong>Data</strong>: """ + item['date'].strftime("%m/%d/%Y, %H:%M:%S") + """&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>Total</strong>: R$""" + str("{:.2f}".format(item['total'])) + """&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>Frete</strong>: R$""" + str("{:.2f}".format(item['frete'])) + """</p>
                <p><strong>Cliente</strong>: </p>
                <p><strong>Nome</strong>: """ + item['nome'] + """ </p>
                <p><strong>Telefone</strong>: """ + item['telefone'] + """ &nbsp;&nbsp;&nbsp;&nbsp; 
                    <strong>Celular</strong>: """ + item['telefone1'] + """ </p>
                <p><strong>E-mail</strong>: """ + item['email'] + """ </p>
                <hr>
                """
            html = html + linha

        for item in pedidos:
            linha = """
                <p><strong>Código de compra</strong>: """ + item['codigo_de_compra'] + """ </p>
                <p><strong>Data</strong>: """ + item['date'].strftime("%m/%d/%Y, %H:%M:%S") + """&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>Total</strong>: R$""" + str("{:.2f}".format(item['total'])) + """&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>Frete</strong>: R$""" + str("{:.2f}".format(item['frete'])) + """</p>
                <p><strong>Cliente</strong>: </p>
                <p><strong>Nome</strong>: """ + item['nome'] + """ </p>
                <p><strong>Telefone</strong>: """ + item['telefone'] + """ &nbsp;&nbsp;&nbsp;&nbsp; 
                    <strong>Celular</strong>: """ + item['telefone1'] + """ </p>
                <p><strong>E-mail</strong>: """ + item['email'] + """ </p>
                <hr>
                """
            html = html + linha
            
        for item in pedidos:
            linha = """
                <p><strong>Código de compra</strong>: """ + item['codigo_de_compra'] + """ </p>
                <p><strong>Data</strong>: """ + item['date'].strftime("%m/%d/%Y, %H:%M:%S") + """&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>Total</strong>: R$""" + str("{:.2f}".format(item['total'])) + """&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>Frete</strong>: R$""" + str("{:.2f}".format(item['frete'])) + """</p>
                <p><strong>Cliente</strong>: </p>
                <p><strong>Nome</strong>: """ + item['nome'] + """ </p>
                <p><strong>Telefone</strong>: """ + item['telefone'] + """ &nbsp;&nbsp;&nbsp;&nbsp; 
                    <strong>Celular</strong>: """ + item['telefone1'] + """ </p>
                <p><strong>E-mail</strong>: """ + item['email'] + """ </p>
                <hr>
                """
            html = html + linha


    apiKey = '70065a4d-a395-4a30-a434-e973e3f16827'
    options = {}
    options['apiKey'] = apiKey
    options['value'] = html
    options['MarginLeft'] = 10
    options['MarginRight'] = 10
    options['MarginTop'] = 10
    options['MarginBottom'] = 10
    options['fileName'] = 'Relatorios_de_Pedidos_' + str(datetime.now().strftime("%m/%d/%Y")) + '.pdf'
    res = requests.post('https://api.html2pdfrocket.com/pdf', data=options)
    x = make_response(res.content)
    x.content_type = 'application/pdf'
    x.mimetype = 'application/pdf'
    return x