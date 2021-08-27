from flask import Flask, render_template
from pizza.pizza import pizzaBP



app = Flask(__name__)
app.register_blueprint(pizzaBP)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)