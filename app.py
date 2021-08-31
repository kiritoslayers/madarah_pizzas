from flask import Flask, render_template, Blueprint, request
from pizza.pizza import pizzaBP
import flask
import psycopg2
import psycopg2.extras



app = Flask(__name__)
app.register_blueprint(pizzaBP)

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
pizzaBP = Blueprint('pizza', __name__, template_folder='templates', static_folder='static')

connection = psycopg2.connect(POSTGRESQL_URI)

@app.route('/')
def index():
    with connection.cursor() as cursor:
        sql = """SELECT sabor, descricao, valor, url_foto from madarah.tb_pizza order by id_pizza"""
        cursor.execute(sql)
        lista = rows_to_dict(cursor.description, cursor.fetchall())
    return render_template('index.html', pizzas=lista)

@app.route('/meu-carrinho')
def carrinho():
    return render_template('carrinho.html')


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


if __name__ == "__main__":
    app.run(debug=True)