from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)
    babel.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .carts import bp as carts_bp
    app.register_blueprint(carts_bp)

    from .messaging import bp as messaging_bp
    app.register_blueprint(messaging_bp)
    
    from .inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)

    from .orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    return app
