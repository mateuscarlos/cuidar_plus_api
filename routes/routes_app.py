from flask import Blueprint, render_template

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def index():
    return render_template('index.html')

@app_routes.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app_routes.route('/cadastro_usuarios')
def cadastro_usuarios():
    return render_template('cadastro_usuarios.html')