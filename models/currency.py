from datetime import datetime, timezone
from config.database import db

class Currency(db.Model):
    __tablename__ = "currencies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    code = db.Column(db.String(3), unique=True)
    name = db.Column(db.String(320), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Currency {self.code} - {self.code}>"
