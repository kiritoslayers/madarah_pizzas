import cliente
from functions.functions import row_to_dict, rows_to_dict, tuple_to_dict
from flask import Blueprint, render_template, request, session, redirect
import flask
import os
import psycopg2
import psycopg2.extras
from functions import *
from pagseguro import PagSeguro
import random
from datetime import datetime
import requests
import json

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
carrinhoBP = Blueprint('carrinho', __name__, template_folder='templates', static_folder='static')

config = {'sandbox': True}
# pg = PagSeguro(email="madarah.impacta@gmail.com", token="45B4AE1FB8684648B476ACA83627DA1D")
pg = PagSeguro(email="v94208027278758069937@sandbox.pagseguro.com.br", token="4F540BCC2828D389943F6F9687FD198B")

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
connection = psycopg2.connect(POSTGRESQL_URI)

headers = {}
headers['Authorization'] = "Bearer 4F540BCC2828D389943F6F9687FD198B"
headers['Accept'] = "appplication/json"
headers['Content-Type'] = "appplication/json"
# r = requests.post('https://sandbox.api.pagseguro.com/public-keys', json={}, headers=headers  )


r = requests.post('https://sandbox.api.pagseguro.com/oauth2/application', json={
    "name": 'Madarah pizzas',
    "description": 'Delivery de pizzas',
    "site": 'http://127.0.0.1:5000/',
    "redirect_uri": 'http://127.0.0.1:5000/',
    "logo": 'https://www.meliuz.com.br/blog/wp-content/uploads/2020/02/sabores-pizza-sao-paulo.jpg'

}, headers=headers)

@carrinhoBP.route('/carrinho/aside/<id_cliente>', methods=['GET'])
def list_aside(id_cliente):
    with connection.cursor() as cursor:
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
        cursor.execute(sql, id_cliente)
        lista = rows_to_dict(cursor.description, cursor.fetchall())
        total = 0
        for i in lista:
            i['total_item'] = round(float(i['total_item']), 3)
            total = total + i['total_item']
        if(len(lista) > 0):
            total = round(float(total), 3)


    return render_template("aside.html", itens=lista, total=total)


@carrinhoBP.route('/carrinho/adicionar/<id_pizza>/<id_cliente>', methods=['POST'])
def adicionar(id_pizza, id_cliente):
    with connection.cursor() as cursor:
        sql = """SELECT * FROM madarah.tb_item_carrinho WHERE id_cliente = %s AND id_pizza = %s LIMIT 1"""
        cursor.execute(sql, (id_cliente, id_pizza))
        item = row_to_dict(cursor.description, cursor.fetchone())
        if item:
            quantidade = int(item['quantidade']) + 1
            sql = """UPDATE madarah.tb_item_carrinho SET quantidade = %s WHERE id_item_carrinho = %s"""
            cursor.execute(sql, (quantidade, item['id_item_carrinho']))
        else:    
            sql = """INSERT INTO madarah.tb_item_carrinho (id_pizza, id_cliente, quantidade) VALUES (%s, %s, %s)"""
            cursor.execute(sql, (id_pizza, id_cliente, 1))

        connection.commit()
    return 'ok'




@carrinhoBP.route('/carrinho/set_quantidade/<id>/<qtd>', methods=['POST'])
def set_quantidade(id, qtd): 
    with connection.cursor() as cursor:
        sql = """SELECT * FROM madarah.tb_item_carrinho WHERE id_item_carrinho = %s LIMIT 1"""
        cursor.execute(sql, (id))
        item = row_to_dict(cursor.description, cursor.fetchone())
        if item:
            if (qtd == '0'):
                sql = """DELETE FROM madarah.tb_item_carrinho WHERE id_item_carrinho = %s"""
                cursor.execute(sql, id)
            else:
                sql = """UPDATE madarah.tb_item_carrinho SET quantidade = %s WHERE id_item_carrinho = %s"""
                cursor.execute(sql, (qtd, id))
        else:    
            return os.abort()

        connection.commit()
        return 'ok'
    


@carrinhoBP.route('/carrinho/finalizar', methods=['POST'])
def finalizar():
    cliente = session['cliente']
    usuario = session['usuario']
    if(not(cliente) or not(usuario)):
        return os.abort

    if(cliente['telefone'] == '' or not(cliente['telefone'])):
        return os.abort


    pg.sender = {
        "name": usuario['nome'],
        "area_code": cliente['telefone1'].split(')')[0].replace('(', ''),
        "phone": cliente['telefone1'].split(')')[1],
        "email": usuario['email'],
    }

    # endereco de entrega
    pg.shipping = {
        "type": pg.NONE,
        "street": cliente['type'] + ' ' + cliente['street'],
        "number": cliente['number'],
        "complement": cliente['complement'],
        "district": cliente['district'],
        "postal_code": cliente['postal_code'],
        "city": cliente['city'],
        "state": cliente['state'],
        "country": cliente['country']
    }
    pg.reference_prefix = None # prefixo do codigo da compra
    pg.extra_amount = 12.70 # Valor extra (taxa de entrega - Float (positivo ou negativo)) 
    
    with connection.cursor() as cursor:
        sql = """SELECT 
                          c.id_item_carrinho
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
                    "ammount": item['valor'],
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
        sql = """INSERT INTO madarah.tb_pedido (id_cliente, total, codigo_de_compra, date) VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (str(cliente['id_cliente']), total, pg.reference, datetime.now()))
        connection.commit()
        
        sql = """SELECT * FROM madarah.tb_pedido WHERE codigo_de_compra = '""" + codigo + """' LIMIT 1"""
        cursor.execute(sql)
        pedido = row_to_dict(cursor.description, cursor.fetchone())

        for item in lista:
            item['id_pedido'] = pedido['id_pedido']
            sql = """INSERT INTO madarah.tb_pedido_pizza_rel (id_pizza, id_pedido, quantidade) VALUES (%s, %s, %s)"""
            cursor.execute(sql, (item['id_pizza'], item['id_pedido'], item['quantidade']))
            connection.commit()

        pg.redirect_url = "http://127.0.0.1:5000/pedido/pedido-finalizado/" + str(pedido['id_pedido']) # URL de redirecionamento ("http://meusite.com/obrigado")
        pg.abandon_url = "";
        pg.checkout_session = "";


        response = pg.checkout(True)
    return redirect('')

