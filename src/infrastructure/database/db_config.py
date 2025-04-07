from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Inicializa o banco de dados com o app Flask"""
    db.init_app(app)