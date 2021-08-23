from flask import Flask, render_template
import psycopg2


app = Flask(__name__)
POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"

connection = psycopg2.connect(POSTGRESQL_URI)

try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE madarah.teste (name varchar, idade int);"
            )
except psycopg2.errors.DuplicateTable:
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return '<h1> Aqui é o cadastro </h1>'

if __name__ == "__main__":
    app.run(debug=True)