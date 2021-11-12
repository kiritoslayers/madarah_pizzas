from functions.functions import row_to_dict, rows_to_dict, tuple_to_dict
from flask import Blueprint, render_template, request
import flask
import os
import psycopg2
import psycopg2.extras
from functions import *

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
carrinhoBP = Blueprint('carrinho', __name__, template_folder='templates', static_folder='static')


POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
connection = psycopg2.connect(POSTGRESQL_URI)


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
    
