from flask import Flask, render_template


app = Flask(__name__)

# pagina principal
@app.route("/")
def home():
    return render_template('home.html')

# pagina de contato
@app.route("/contato")
def contato():
    return render_template('contato.html')


if __name__ == '__main__':
    app.run(debug=True)