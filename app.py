from flask import Flask
from flask_cors import CORS
from db import db
from routes.user_routes import user_routes
from routes.routes_app import app_routes
from flasgger import Swagger

app = Flask(__name__, template_folder='../cuidar_plus', static_folder='../cuidar_plus/static')
app.config["SWAGGER"] = {"title": "API Cuidar+", "uiversion": 3, "debug": True}
Swagger(app)

CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})

# Configuração SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise RuntimeError('No database URI provided')

db.init_app(app)

with app.app_context():
    db.create_all()

# Registro de rotas
app.register_blueprint(app_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)
