from datetime import datetime, timezone
from config.database import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=True)
    price = db.relationship(
        "ProductPricing", back_populates="product", cascade="all, delete-orphan"
    )
    plan_id = db.Column(
        db.Integer, db.ForeignKey("plans.id", ondelete="CASCADE"), nullable=False
    )
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    plan = db.relationship("Plan", back_populates="products")

    def __repr__(self):
        return f"<Product {self.id} - {self.name}>"
