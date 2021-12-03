from pyasn1.type.univ import Null
from functions.functions import row_to_dict, rows_to_dict, tuple_to_dict
from flask import Flask, render_template
from flask_login import LoginManager, login_manager, login_user
from pizza.pizza import pizzaBP
from carrinho.carrinho import carrinhoBP
from cliente.cliente import clienteBP
from pedido.pedido import pedidoBP
import psycopg2
import psycopg2.extras
from functions import *
from flask_admin import Admin

import os
import pathlib
from google import auth

import requests
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pagseguro import PagSeguro
from perfil.perfil import perfilBP


app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "CodeSpecialist.com"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "255715985919-6rjumhu5881vldgqdkjh7i558o7h3cso.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


app.config['FLASK_ADMIN_SWATCH'] = 'united'
admin = Admin(app, name='Pizza For Fun', template_mode='bootstrap3')
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(carrinhoBP)
app.register_blueprint(clienteBP)
app.register_blueprint(pedidoBP)
app.register_blueprint(perfilBP)
app.register_blueprint(pizzaBP)

POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
connection = psycopg2.connect(POSTGRESQL_URI)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route('/')
def index():
    authenticate =  session if 'google_id' in session else False
    
    with connection.cursor() as cursor:
        cursor.execute('''SELECT * from madarah.tb_pizza order by id_pizza''')
        lista = rows_to_dict(cursor.description, cursor.fetchall())
        cliente = False
        user = False
        if authenticate:
            sql = """SELECT * FROM madarah.tb_usuario WHERE google_id = '""" + authenticate['google_id'] + """' LIMIT 1"""
            cursor.execute(sql)
            user = tuple_to_dict(cursor.description, cursor.fetchone())
            if(user):
                session['id_usuario'] = user['id_usuario']

            sql = """SELECT * FROM madarah.tb_cliente WHERE id_usuario = """ + str(user['id_usuario']) + """ LIMIT 1"""
            cursor.execute(sql)
            cliente = tuple_to_dict(cursor.description, cursor.fetchone())
            if(cliente):
                session['id_cliente'] = cliente['id_cliente']

        session['usuario'] = user
        session['cliente'] = cliente

    return render_template('index.html', pizzas=lista, auth=authenticate, cliente=cliente, usuario=user)

    

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)



@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    google_id = session["google_id"]
    name = session["name"]
    email = session["email"]
    with connection.cursor() as cursor:
        sql = """SELECT * FROM madarah.tb_usuario WHERE google_id = '""" + google_id + """' LIMIT 1"""
        cursor.execute(sql)
        user = tuple_to_dict(cursor.description, cursor.fetchone())
        if user == None:
            sql = """INSERT INTO madarah.tb_usuario (nome, email, role, google_id) VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (name, email, 'cliente', google_id))
            connection.commit()
            sql = """SELECT * FROM madarah.tb_usuario WHERE google_id = '""" + google_id + """' LIMIT 1"""
            cursor.execute(sql)
            user = tuple_to_dict(cursor.description, cursor.fetchone())
            cursor.close()
            session["role"] = 'cliente'
        else:
            session['role'] = user['role']
           
        sql = """SELECT * FROM madarah.tb_cliente WHERE id_usuario = """ + str(user['id_usuario']) + """ LIMIT 1"""
        cursor.execute(sql)
        cliente = tuple_to_dict(cursor.description, cursor.fetchone())
        if(cliente == None):
            sql = """INSERT INTO madarah.tb_cliente (id_usuario
                                            , nome
                                            , telefone
                                            , telefone1) 
                    VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (user['id_usuario'], user['nome'], '', ''))
            connection.commit()  
        
        sendEmail(session['name'],session['email'], 'logout')        

    return redirect("/")


@app.route("/logout")
def logout():
    # sendEmail(session['name'],session['email'], 'logout')
    session.clear()
    return redirect("/")


@app.route("/profile")
@login_is_required
def protected_area():
    name = session['name']
    authenticate =  session['name'] if 'google_id' in session else False
    return render_template('/', name=name, auth=authenticate)

def sendEmail(nome, email, acao):
    host = 'smtp.gmail.com'
    port = '587'
    login = 'madarah.impacta@gmail.com'
    senha = 'cadomeew'

    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.login(login, senha)

    body = f'Você fez {acao} com {nome} - {email}'
    subject = 'AC02 - Madarah SPTM'

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = email
    email_msg['Subject'] = subject
    email_msg.attach(MIMEText(body, 'Plain'))


    server.sendmail(
        email_msg['From'],
        email_msg['To'],
        email_msg.as_string()
    )
    server.quit()



if __name__ == "__main__":
    app.run(debug=True)
