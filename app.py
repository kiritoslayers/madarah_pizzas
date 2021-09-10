from functions.functions import rows_to_dict
from flask import Flask, render_template
from flask_login import LoginManager, login_manager, login_user
from pizza.pizza import pizzaBP
from login.login import loginBP
from usuario.usuario import userBP
import psycopg2
import psycopg2.extras
from functions import *
from flask_admin import Admin



app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'united'
admin = Admin(app, name='Pizza For Fun', template_mode='bootstrap3')
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(pizzaBP)
app.register_blueprint(userBP)
app.register_blueprint(loginBP)



POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"



connection = psycopg2.connect(POSTGRESQL_URI)

@app.route('/')
def index():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT sabor, descricao, valor, url_foto from madarah.tb_pizza order by id_pizza''')
        lista = rows_to_dict(cursor.description, cursor.fetchall())
    return render_template('index.html', pizzas=lista)


if __name__ == "__main__":
    app.run(debug=True)
