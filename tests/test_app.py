import time
import pytest
from datetime import datetime, timedelta, timezone
from config.database import db
from models import Subscription, Customer, Product, ProductPricing, Plan
from repositories import SubscriptionRepository
from app import create_app

@pytest.fixture(scope="function")
def test_app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "API_TITLE": "Clue Insights API Tests",
        "API_VERSION": "v0.0.1",
        "OPENAPI_VERSION": "3.1.0",
        "OPENAPI_URL_PREFIX": "/doc",
        "OPENAPI_SWAGGER_UI_PATH": "/",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    }

    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def session(test_app):
    with test_app.app_context():
        yield db.session


@pytest.fixture
def test_customer(session):
    customer = Customer(
        email="email@email.com",
        first_name="John",
        last_name="Doe",
        phone="911",
        country="Nigeria",
        password_hash="$2b$12$vk1pq7jpPkDOQ/9//mIKsuwzDP60xlOLTIrOWypJwZlEN97Sfpg1O",
        currency_code="USD",
        created_at=datetime.now(timezone.utc),
    )
    session.add(customer)
    session.commit()
    return customer


@pytest.fixture
def test_plan(session):
    plan = Plan(billing_interval=30, created_at=datetime.now(timezone.utc))
    session.add(plan)
    session.commit()
    return plan


@pytest.fixture
def test_product(session, test_plan):
    product = Product(
        name="Basic Plan",
        description="Just a basic plan",
        price=[
            ProductPricing(
                price=100,
                currency="USD",
                from_date=datetime.now().date(),
                to_date=datetime.now().date(),
                created_at=datetime.now(timezone.utc),
            )
        ],
        plan_id=test_plan.id,
        created_at=datetime.now(timezone.utc),
    )
    session.add(product)
    session.commit()
    return product


# -------------------------
# Tests
# -------------------------


def test_purchase_subscription(session, test_customer, test_product):
    data = {"product_id": test_product.id, "validity_period": 30, "price": 100}
    subscription = SubscriptionRepository.purchase_subscription(test_customer.id, data)

    assert subscription is not None, "Subscription should be created"
    assert subscription.customer_id == test_customer.id
    assert subscription.status == "active"
    assert subscription.ends_at > subscription.starts_at


def test_cancel_subscription(session, test_customer, test_product):
    data = {"product_id": test_product.id, "validity_period": 30, "price": 100}
    SubscriptionRepository.purchase_subscription(test_customer.id, data)
    cancelled = SubscriptionRepository.cancel_subscription(test_customer.id)

    assert cancelled is not None, "Subscription should be returned after cancellation"
    assert cancelled.cancelled_at is not None, "Cancelled timestamp should be set"
    assert (
        cancelled.status == "active"
    ), "Subscription should still be active after cancellation"


def test_get_active_subscriptions(session, test_customer, test_product):
    # Create a 12 new subscriptions to simulate real data
    for _ in range(12):
        SubscriptionRepository.purchase_subscription(
            test_customer.id,
            {"product_id": test_product.id, "validity_period": 30, "price": 100},
        )

    start_time = time.perf_counter()
    response = SubscriptionRepository.get_active_subscriptions()
    end_time = time.perf_counter()
    duration = end_time - start_time

    assert isinstance(response, list), " Response should be a list"
    assert len(response) > 0, "Response should contain at least one subscription"
    assert all(
        sub.status == "active" for sub in response
    ), "All subscriptions should have the status == active"

    assert len(response) == 10, "Response should contain exactly 10 suscriptions due to the LIMIT parameter in the query"

    assert duration < 0.1, "Query should run to completion in less than a second"

def test_list_subscriptions(session, test_customer, test_product):
    # Create a 12 new subscriptions to simulate real data
    for _ in range(12):
        SubscriptionRepository.purchase_subscription(
            test_customer.id,
            {"product_id": test_product.id, "validity_period": 30, "price": 100},
        )

    start_time = time.perf_counter()
    response = SubscriptionRepository.list_subscriptions()
    end_time = time.perf_counter()
    duration = end_time - start_time

    assert isinstance(response, list), " Response should be a list"
    assert len(response) > 0, "Response should contain at least one subscription"
    assert (
        len(response) == 10
    ), "Response should contain exactly 10 suscriptions due to the LIMIT parameter in the query"
    assert duration < 0.1, "Query should run to completion in less than a second"

def test_retrieve_customer_subscription_history(session, test_customer, test_product):
    # Create a 12 new subscriptions to simulate real data
    for _ in range(12):
        SubscriptionRepository.purchase_subscription(
            test_customer.id,
            {"product_id": test_product.id, "validity_period": 30, "price": 100},
        )

    start_time = time.perf_counter()
    response = SubscriptionRepository.retrieve_customer_subscription_history(
        test_customer.id
    )
    end_time = time.perf_counter()
    duration = end_time - start_time

    assert isinstance(response, list), "Response should be a list"
    assert len(response) > 0, " should contain at least one subscription"
    assert all(
        sub.customer_id == test_customer.id for sub in response
    ), "All subscriptions should belong to the customer"

    assert (
        len(response) == 10
    ), "Response should contain exactly 10 suscriptions due to the LIMIT parameter in the query"

    assert duration < 0.1, "Query should run to completion in less than a second"
