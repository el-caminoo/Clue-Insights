from sqlalchemy import text
from datetime import datetime, timezone, timedelta
from models import Subscription
from config.database import db

class SubscriptionRepository:

    @staticmethod
    def _get_utc_now():
        return datetime.now(timezone.utc)

    @staticmethod
    def _save(instance):
        db.session.add(instance)
        db.session.commit()
        return instance

    @staticmethod
    def _get_active_subscription(customer_id):
        now = SubscriptionRepository._get_utc_now()
        return (
          db.session.query(Subscription)
          .filter(
              Subscription.customer_id == customer_id,
              Subscription.status == "active",
              Subscription.starts_at <= now,
              Subscription.ends_at >= now,
          )
          .first()
      )

    @staticmethod
    def purchase_subscription(customer_id, data: dict):
        """Creates a new active subscription."""
        now = SubscriptionRepository._get_utc_now()

        new_subscription = Subscription(
        status="inactive",
        customer_id=customer_id,
        product_id=data["product_id"],
        starts_at=now,
        created_at=now,
    )

        SubscriptionRepository._save(new_subscription)

        # subscription status, starts_at and ends_at fields are updated after the invoice has been paid(usually on the same day or immediately)
        # and payment confirmation via webhook or other means depending on the payment processor(e.g stripe).
        # This is just a simulation of the process.

        new_subscription.status = "active"
        new_subscription.starts_at = now

        # adds the validity period of the product(30 days) to the timestamp as at the time of payment confirmation
        new_subscription.ends_at = now + timedelta(days=data["validity_period"])
        db.session.commit()
        return new_subscription

    @staticmethod
    def upgrade_subscription(customer_id, data: dict):
        """Upgrades an active subscription to a new one."""
        now = SubscriptionRepository._get_utc_now()

        # Marks the active subscription as upgraded, also specifies the product to be upgraded to and when it was upgraded.
        current = SubscriptionRepository._get_active_subscription(customer_id)
        if current:
            current.status = "upgraded"
            current.upgraded_at = now
            current.upgraded_to_product_id = data["product_id"]
            db.session.commit()
        else:
            db.session.rollback()

        # Creates a new subscription row with information relating to the newly upgraded plan and marks as active. Depending on business practices
        # and other factors, upgrades may not always be instant and payment may be required before upgrade is carried out.
        upgraded = Subscription(
        status="active",
        customer_id=customer_id,
        product_id=data["product_id"],
        starts_at=now,
        ends_at=now + timedelta(days=data["validity_period"]),
        created_at=now,
    )

        SubscriptionRepository._save(upgraded)
        return upgraded

    @staticmethod
    def cancel_subscription(customer_id):
        now = SubscriptionRepository._get_utc_now()

        # Canceling a subscription just updates the cancelled_at field in the active subscription row with the timestamp of when the request was made.
        # hence the row won't be returned when the query to return rows for subscription renewal is ran either as a Cron Job or other means.
        current = SubscriptionRepository._get_active_subscription(customer_id)
        if current:
            current.cancelled_at = now
            db.session.commit()

        return current

    @staticmethod
    def get_active_subscriptions(limit=10, offset=0):

        sql = text("""
        SELECT id FROM subscriptions
        WHERE status = 'active'
          AND deleted_at IS NULL
          AND (ends_at IS NULL OR ends_at > :now)
        ORDER BY starts_at DESC
        LIMIT :limit OFFSET :offset
        """)
        now = datetime.now(timezone.utc)

        result = db.session.execute(sql, {
        "now": now,
        "limit": limit,
        "offset": offset
        })

        ids = [row.id for row in result]
        if not ids:
            return []

        # Fetches ORM instances to ensure the result is returned as an instance of the model for effective object serialization.
        subscriptions = (
            db.session.query(Subscription)
            .filter(Subscription.id.in_(ids))
            .order_by(Subscription.starts_at.desc())
            .all()
        )

        return subscriptions

    @staticmethod
    def list_subscriptions(limit=10, offset=0):

        sql = text(
            """
        SELECT id FROM subscriptions
        WHERE deleted_at IS NULL
        ORDER BY starts_at DESC
        LIMIT :limit OFFSET :offset
        """
        )

        result = db.session.execute(sql,{"limit": limit, "offset": offset})

        ids = [row.id for row in result]
        if not ids:
            return []

        # Return actual model instances, ordered by starts_at descending for effective serialization.
        subscriptions = (
            db.session.query(Subscription)
            .filter(Subscription.id.in_(ids))
            .order_by(Subscription.starts_at.desc())
            .all()
        )

        return subscriptions

    @staticmethod
    def retrieve_customer_subscription_history(customer_id, limit=10, offset=0):

        sql = text(
            """
            SELECT id FROM subscriptions
            WHERE customer_id = :customer_id
              AND deleted_at IS NULL
            ORDER BY starts_at DESC
            LIMIT :limit OFFSET :offset
        """
        )

        result = db.session.execute(
            sql, {"customer_id": customer_id, "limit": limit, "offset": offset}
        )

        ids = [row.id for row in result]
        if not ids:
            return []

        # Return actual model instances, ordered by starts_at descending for effective serialization.
        subscriptions = (
            db.session.query(Subscription)
            .filter(Subscription.id.in_(ids))
            .order_by(Subscription.starts_at.desc())
            .all()
        )

        return subscriptions

    # SQL queries for retrieving active subscriptions, listing subscriptions and Returning
    # subscription history for a particular customer have all been optimized for better efficiency and
    # speed by doing the following
    # 1. Requesting for specific field and not all fields
    # 2. Filtering results as early as possible using indexed columns
    # 3. Making use of LIMIT to restrict the number of results to be returned at once.
