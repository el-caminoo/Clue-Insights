import pytest
from app import create_app
from config.database import db
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from models import Base  # If you're using declarative base


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()
