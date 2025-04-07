from datetime import datetime, timezone
from config.database import db

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    country = db.Column(db.String(120), nullable=False)
    currency_code = db.Column(
        db.String(3),
        db.ForeignKey("currencies.code", ondelete="RESTRICT"),
        nullable=False,
    )
    password_hash = db.Column(db.String(256), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    currency = db.relationship("Currency", backref="customers")

    subscriptions = db.relationship(
        "Subscription", back_populates="customer", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"
