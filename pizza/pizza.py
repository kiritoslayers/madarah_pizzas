from flask import Blueprint, render_template
import psycopg2


POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
connection = psycopg2.connect(POSTGRESQL_URI)



pizzaBP = Blueprint('pizza', __name__, template_folder='templates', static_folder='static')


@pizzaBP.route('/cardapio_pizza')
def home_pizza():
    return 'cardapio de pizza'


@pizzaBP.route('/cadastro_pizza')
def cadastro_pizza():
    return render_template('cadastro.html')


@pizzaBP.route('/edicao_pizza')
def edicao_pizza():
    return 'edicao_pizza'


