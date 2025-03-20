from .create_user import create_user_bp
from .delete_user import delete_user_bp
from .get_users import get_users_bp
from .update_user import update_user_bp

def register_user_routes(app):
    app.register_blueprint(create_user_bp)
    app.register_blueprint(delete_user_bp)
    app.register_blueprint(get_users_bp)
    app.register_blueprint(update_user_bp)

