import uuid

from util.deployment import Deployment

deployment = Deployment().deployment


def generate_uuid():
    _uuid = str(uuid.uuid4())
    return _uuid


def generate_cookie(name, response):
    cookie_id = generate_uuid()
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
    IS_PRODUCTION = deployment == "cloud"
    response.set_cookie(
        "auth_cookie",
        access_token,
        max_age=30 * 24 * 60 * 60,  # 30 days
        httponly=True,
        secure=IS_PRODUCTION,  # True in production (HTTPS), False locally
        samesite="None"
        if IS_PRODUCTION
        else "Lax",  # None for cross-site in prod, Lax for local
        path="/",
    )
    return access_token


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
