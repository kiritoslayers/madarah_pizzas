from flask import Blueprint, render_template, request
import flask
import psycopg2
import psycopg2.extras


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
        valor = float(request.form['valor'])
        url_foto = str(request.form['url_foto'])
        connection = psycopg2.connect(POSTGRESQL_URI)
        with connection.cursor() as cursor:
            sql = """insert into madarah.tb_pizza (sabor, descricao, valor, url_foto) VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (sabor, descricao, valor, url_foto))
            cursor.close()
            connection.commit()
    
    return render_template('cadastro.html')



@pizzaBP.route('/editar_pizza', methods=['POST', 'GET'])
def edicao_pizza():
    if flask.request.method == 'POST':
        id_form = int(request.form['id']),
        sabor = str(request.form['sabor']),
        descricao = str(request.form['descricao']),
        valor = float(request.form['valor'])
        url_foto = str(request.form['url_foto'])
        connection = psycopg2.connect(POSTGRESQL_URI)
        with connection.cursor() as cursor:
            sql = """update madarah.tb_pizza SET sabor = (%s), descricao = (%s), valor = (%s), url_foto = (%s) WHERE id_pizza = (%s)"""
            cursor.execute(sql, (sabor, descricao, valor, url_foto, id_form))
            cursor.close()
            connection.commit()
    return render_template('edicao.html')



# @pizzaBP.route('/delete_pizza/<int:id>', methods=['POST', 'GET'])
# def delete_pizza(id):
#     id_pizza = flask.request.args.get('id')
#     connection = psycopg2.connect(POSTGRESQL_URI)
#     with connection.cursor() as cursor:
#         sql = """select * from madarah.tb_pizza WHERE id_pizza = (%s)"""
#         cursor.execute(sql, (id))
#         pizza = cursor.fetchall()
#     return render_template('delete_pizza.html')
        
    

def row_to_dict(description, row):
    if row is None: return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result


