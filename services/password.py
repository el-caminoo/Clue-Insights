import bcrypt

class PasswordService:
    @staticmethod
    def hash_password(password):
        """Hash a password before storing it."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(password, hashed_password):
        """Verify a hashed password."""
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))