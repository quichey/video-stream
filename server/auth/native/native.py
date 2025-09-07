import bcrypt
from typing_extensions import override
from typing import Literal

from sqlalchemy.orm import Session

from auth.Auth import Auth
from api.util.request_data import extract_registration_info, extract_login_info
from db.Schema.Models import User


class NativeAuth(Auth):
    @override
    def register(self, request, response) -> User | Literal[False]:
        registration_info = extract_registration_info(request)
        hashed_pw = self.hash_password(registration_info["password"])
        return self.store_user_record(registration_info["name"], hashed_pw)

    @override
    def login(self, request, response) -> User | Literal[False]:
        login_info = extract_login_info(request)
        user_name = login_info["name"]
        user_instance = self.get_user_instance(user_name)
        stored_hash = user_instance.password
        plain_password = login_info["password"]
        if self.verify_password(plain_password, stored_hash):
            return user_instance
        else:
            return False

    @override
    def logout(self, request, response):
        pass

    # User registers -> hash their password
    def hash_password(self, plain_password: str) -> bytes:
        # bcrypt automatically generates a random salt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed

    # User logs in -> verify their password against stored hash
    def verify_password(self, plain_password: str, stored_hash: bytes) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash)

    def get_user_instance(self, user_name) -> User:
        user_record = None
        with Session(self.engine) as session:
            user_record = session.query(User).filter_by(name=user_name).first()
        return user_record

    def store_user_record(self, name, password) -> User | Literal[False]:
        # also save to mysql db
        with Session(self.engine) as session:
            new_user = User(
                name=name,
                password=password,
            )
            session.add(new_user)
            session.commit()
            if new_user.id is not None:
                return new_user

        return False

    def verify_user_name_unique(self, user_name) -> bool:
        user_record = None
        with Session(self.engine) as session:
            user_record = session.query(User).filter_by(name=user_name).first()
        return user_record is None


NATIVE_AUTH = NativeAuth()
