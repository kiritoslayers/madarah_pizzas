from flask import Flask, render_template
from pizza.pizza import pizzaBP
import psycopg2


app = Flask(__name__)


POSTGRESQL_URI = "postgres://nrzaptwjbceonc:85e6f9cb1eb0447157fa9de8cc08cd804f02a1e555b5747860ec3a6d9f9140a0@ec2-35-153-91-18.compute-1.amazonaws.com:5432/d939kg82f0uljg"
connection = psycopg2.connect(POSTGRESQL_URI)


app.register_blueprint(pizzaBP)


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)