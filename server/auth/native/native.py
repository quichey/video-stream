import bcrypt
from typing_extensions import override

from sqlalchemy.orm import Session

from auth.Auth import Auth
from api.util.request_data import extract_registration_info
from db.Schema.Models import User

class NativeAuth(Auth):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    @override
    def register(self, request, response):
        registration_info = extract_registration_info(request)
        hashed_pw = self.hash_password(registration_info["password"])
        self.store_user_record(registration_info["name"], hashed_pw)
        #TODO: add something to response?

    @override
    def login(self, request, response):
        pass

    @override
    def logout(self, request, response):
        pass

    # User registers -> hash their password
    def hash_password(plain_password: str) -> bytes:
        # bcrypt automatically generates a random salt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed

    # User logs in -> verify their password against stored hash
    def verify_password(plain_password: str, stored_hash: bytes) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash)
    
    def store_user_record(self, name, password):
        new_user = User(
            name=name,
            password=password,
        )
        # also save to mysql db
        with Session(self.engine) as session:
            session.add(new_user)
            session.commit()
        return "ok"