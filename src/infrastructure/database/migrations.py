from flask_migrate import Migrate
from src.interfaces.api.app import app
from src.infrastructure.database.db_config import db

migrate = Migrate(app, db)

def init_migrations(app):
    return Migrate(app, db)