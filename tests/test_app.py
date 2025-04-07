# import pytest
# from datetime import datetime, timedelta, timezone
# from config.database import db
# from models import Subscription, Customer, Product, ProductPricing
# from repositories import SubscriptionRepository
# from app import create_app


# @pytest.fixture(scope="module")
# def test_app():
#     app = create_app()
#     app.config.update(
#         {
#             "TESTING": True,
#             "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
#         }
#     )

#     with app.app_context():
#         db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()


# @pytest.fixture
# def session(test_app):
#     with test_app.app_context():
#         yield db.session


# @pytest.fixture
# def test_customer(session):
#     customer = Customer(
#         email="test@example.com",
#         password_hash="hashed",
#         created_at=datetime.now(timezone.utc),
#     )
#     session.add(customer)
#     session.commit()
#     return customer


# @pytest.fixture
# def test_product(session):
#     product = Product(
#         name="Basic Plan", description="Just a basic plan", 
#         plan_id=1, created_at=datetime.now(timezone.utc)
#     )
#     session.add(product)
#     session.commit()
#     return product


# def test_purchase_subscription(session, test_customer, test_product):
#     data = {
#         "product_id": test_product.id,
#         "validity_period": test_product.validity_period,
#     }
#     subscription = SubscriptionRepository.purchase_subscription(test_customer.id, data)

#     assert subscription is not None
#     assert subscription.customer_id == test_customer.id
#     assert subscription.status == "active"
#     assert subscription.ends_at > subscription.starts_at


# def test_cancel_subscription(session, test_customer, test_product):
#     # First, purchase a subscription
#     data = {"product_id": test_product.id, "validity_period": 30}
#     SubscriptionRepository.purchase_subscription(test_customer.id, data)

#     # Cancel it
#     cancelled = SubscriptionRepository.cancel_subscription(test_customer.id)

#     assert cancelled is not None
#     assert cancelled.cancelled_at is not None


# def test_retrieve_customer_subscription_history(session, test_customer):
#     history = SubscriptionRepository.retrieve_customer_subscription_history(
#         test_customer.id
#     )
#     assert isinstance(history, list)
#     assert all(sub.customer_id == test_customer.id for sub in history)
