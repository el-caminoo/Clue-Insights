from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy and Migrate instances
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize the database with the given Flask app."""
    db.init_app(app)
    migrate.init_app(app, db)
