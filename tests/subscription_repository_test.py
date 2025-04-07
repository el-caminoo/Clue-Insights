import pytest
from repositories import SubscriptionRepository
from models import Subscription

@pytest.fixture
def dummy_data():
    return {"product_id": 1, "validity_period": 30}


def test_purchase_subscription(db_session, dummy_data):
    customer_id = 1
    subscription = SubscriptionRepository.purchase_subscription(customer_id, dummy_data)

    assert subscription.id is not None
    assert subscription.customer_id == customer_id
    assert subscription.status == "active"
    assert subscription.product_id == dummy_data["product_id"]
    assert subscription.ends_at is not None


def test_cancel_subscription(db_session, dummy_data):
    customer_id = 2
    # Purchase first
    SubscriptionRepository.purchase_subscription(customer_id, dummy_data)

    # Cancel
    cancelled = SubscriptionRepository.cancel_subscription(customer_id)
    assert cancelled.cancelled_at is not None
    assert (
        cancelled.status == "active"
    )  # Status stays the same unless you decide otherwise


def test_upgrade_subscription(db_session, dummy_data):
    customer_id = 3
    SubscriptionRepository.purchase_subscription(customer_id, dummy_data)

    new_plan = {"product_id": 2, "validity_period": 45}

    upgraded = SubscriptionRepository.upgrade_subscription(customer_id, new_plan)

    assert upgraded.product_id == 2
    assert upgraded.status == "active"
    assert upgraded.ends_at is not None
