from datetime import datetime, timezone
from config.database import db


class Plan(db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    billing_interval = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    products = db.relationship(
        "Product", back_populates="plan", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Plan {self.id} - Product ID {self.product_id} - Interval {self.billing_interval}>"
