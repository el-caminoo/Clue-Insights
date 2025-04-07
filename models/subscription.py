from datetime import datetime, timezone
from config.database import db


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Enum("inactive", "cancelled", "active", "upgraded", name="subscription_status"),nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id", ondelete="NO ACTION"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="NO ACTION"), nullable=False)
    starts_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    ends_at = db.Column(db.DateTime, nullable=True, index=True)
    downgraded_at = db.Column(db.DateTime, nullable=True)
    downgraded_to_product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="NO ACTION"), nullable=True
    )
    upgraded_at = db.Column(db.DateTime, nullable=True)
    upgraded_to_product_id = db.Column(
        db.Integer, db.ForeignKey("products.id", ondelete="NO ACTION"), nullable=True
    )
    cancelled_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)

    customer = db.relationship("Customer", back_populates="subscriptions", lazy=True)
    product = db.relationship(
        "Product", foreign_keys=[product_id], backref="subscriptions", lazy=True
    )
    downgraded_to_product = db.relationship(
        "Product",
        foreign_keys=[downgraded_to_product_id],
        backref="downgraded_subscriptions",
        lazy=True
    )
    upgraded_to_product = db.relationship(
        "Product",
        foreign_keys=[upgraded_to_product_id],
        backref="upgraded_subscriptions",
        lazy=True,
    )
    
    def __repr__(self):
        return f"<Subscription {self.id} for Customer {self.customer_id}, Status: {self.status}>"
