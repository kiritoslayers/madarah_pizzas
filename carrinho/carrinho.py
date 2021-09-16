from functions.functions import rows_to_dict, tuple_to_dict
from flask import Blueprint, render_template, request
import flask
import psycopg2
import psycopg2.extras
from functions import *

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
carrinhoBP = Blueprint('carrinho', __name__, template_folder='templates', static_folder='static')

@carrinhoBP.route('/carrinho/aside', methods=['GET'])
def list_aside():
    return render_template("aside.html")



@carrinhoBP.route('/carrinho/set_quantidade/<id>/<qtd>', methods=['POST'])
def set_quantidade(id, qtd):
    return 'ok'

