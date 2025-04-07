from flask import Flask
from config.env import Config
from config.database import init_db, db
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_cors import CORS
from routes.user import user_routes
from routes.customer import customer_routes
from routes.product import product_routes
from routes.subscription import subscription_routes


def create_app():
    app = Flask(__name__)

    CORS(app)

    # Load configurations
    app.config.from_object(Config)

    api = Api(app)

    # Initialize database
    init_db(app)

    # Initialize extensions
    JWTManager(app)

    # Register blueprints
    api.register_blueprint(user_routes, url_prefix="/user")
    api.register_blueprint(customer_routes, url_prefix="/customer")
    api.register_blueprint(product_routes, url_prefix="/product")
    api.register_blueprint(subscription_routes, url_prefix="/subscription")

    return app