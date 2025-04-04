from flask import Flask
from config.env import Config
from config.database import init_db
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from routes.user import user_routes
from routes.customer import customer_routes


def create_app():
    """Application factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Load configurations
    app.config.from_object(Config)

    # Initialize database
    init_db(app)

    # Initialize extensions
    JWTManager(app)
    api = Api(app)

    # OpenAPI Specification
    api.spec.options["servers"] = [
        {"url": "http://127.0.0.1:5000", "description": "Local development server"}
    ]

    # Register blueprints
    api.register_blueprint(user_routes, url_prefix="/user")
    api.register_blueprint(customer_routes, url_prefix="/customer")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
