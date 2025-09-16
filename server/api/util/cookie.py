import uuid

from util.deployment import Deployment
from api.util.request_data import attach_data_to_payload

deployment = Deployment().deployment


def generate_uuid():
    _uuid = str(uuid.uuid4())
    return _uuid


def generate_cookie(name, response, value="TBD"):
    cookie_id = generate_uuid() if value == "TBD" else value
    IS_PRODUCTION = deployment == "cloud"
    response.set_cookie(
        name,
        cookie_id,
        max_age=30 * 24 * 60 * 60,  # 30 days
        httponly=True,
        secure=IS_PRODUCTION,  # True in production (HTTPS), False locally
        samesite="None"
        if IS_PRODUCTION
        else "Lax",  # None for cross-site in prod, Lax for local
        path="/",
    )
    return cookie_id


def set_auth_cookie(response, access_token):
    return generate_cookie("auth_cookie", response, value=access_token)


def set_one_time_token(response, one_time_token):
    # Attach the info to payload for React to set
    attach_data_to_payload(response, {"one_time_token": one_time_token})
    return one_time_token


def expire_cookie(name, response):
    IS_PRODUCTION = deployment == "cloud"  # (== not "is")
    response.set_cookie(
        name,
        value="",
        expires=0,  # Expire immediately
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="None" if IS_PRODUCTION else "Lax",
        path="/",
    )
    return
