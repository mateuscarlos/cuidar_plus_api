from .create_user import create_user_bp
from .delete_user import delete_user_bp
from .get_all_users import get_all_users_bp
from .get_user_by_id import get_user_by_id_bp
from .update_user import update_user_bp

def register_user_routes(app):
    app.register_blueprint(create_user_bp)
    app.register_blueprint(delete_user_bp)
    app.register_blueprint(get_all_users_bp)
    app.register_blueprint(get_user_by_id_bp)
    app.register_blueprint(update_user_bp)

