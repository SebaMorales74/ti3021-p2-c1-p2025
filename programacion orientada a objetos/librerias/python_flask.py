from flask import Flask
# Para instalar flask deben de utilizar el comando: pip install flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return {"message":"Hola sección P2-C1 🤖📚🐍"}

if __name__ == '__main__':
    app.run(debug=True)