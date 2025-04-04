from config.database import db


class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False, index=True)
  password_hash = db.Column(db.String(256), nullable=False)
  role = db.Column(db.String(120), nullable=False)

  def __repr__(self):
    return f"<User {self.email}>"
