from datetime import datetime, timezone
from config.database import db

class ProductPricing(db.Model):
    __tablename__ = "products_pricing"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    currency = db.Column(db.String(3), db.ForeignKey("currencies.code", ondelete="RESTRICT"),
        nullable=False,
    )
    price = db.Column(db.Integer, nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    product = db.relationship("Product", back_populates="price", lazy=True)

    def __repr__(self):
        return f"<ProductPricing product_id={self.product_id} price={self.price} from={self.from_date} to={self.to_date}>"


product = db.relationship("Product", back_populates="prices")
