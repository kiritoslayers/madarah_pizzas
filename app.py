from functions.functions import rows_to_dict, tuple_to_dict
from flask import Flask, render_template, Blueprint
from pizza.pizza import pizzaBP
import psycopg2
import psycopg2.extras
from functions import *


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



if __name__ == "__main__":
    app.run(debug=True)