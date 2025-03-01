from flask import Flask
from flask_cors import CORS
from db import db
from routes.user_routes import user_routes
from routes.routes_app import app_routes
from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from config import Config

app = Flask(__name__, template_folder='../cuidar_plus', static_folder='../cuidar_plus/static')
app.config.from_object(Config)
Swagger(app)

CORS(app, resources=Config.CORS_RESOURCES)

# Configurações de segurança
talisman = Talisman(app)
limiter = Limiter(app=app, key_func=get_remote_address)

db.init_app(app)

with app.app_context():
    db.create_all()

# Registro de rotas
app.register_blueprint(app_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)
