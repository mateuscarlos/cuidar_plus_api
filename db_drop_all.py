from app import app
from db import db

with app.app_context():
    db.drop_all()
    print("Todas as tabelas foram removidas.")