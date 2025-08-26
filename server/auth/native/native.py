import bcrypt

class NativeAuth():
    # User registers -> hash their password
    def hash_password(plain_password: str) -> bytes:
        # bcrypt automatically generates a random salt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed

    # User logs in -> verify their password against stored hash
    def verify_password(plain_password: str, stored_hash: bytes) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash)