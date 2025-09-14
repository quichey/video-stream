import uuid
import os

from util.deployment import Deployment
from api.util.request_data import attach_data_to_payload

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
    max_age = 30 * 24 * 60 * 60  # 30 days

    server_domain = (
        "localhost"
        if deployment == "local"
        else os.environ.get("REACT_APP_SERVER_APP_URL")
    )
    if deployment == "cloud":
        server_domain = server_domain[len("https://") :]
    auth_cookie_info = {
        "name": "auth_cookie",
        "value": access_token,
        "max_age": max_age,
        "httponly": True,
        "secure": IS_PRODUCTION,
        "samesite": "None" if IS_PRODUCTION else "Lax",
        "path": "/",
        "domain": server_domain,
    }

    # Attach the info to payload for React to set
    attach_data_to_payload(response, {"auth_cookie_info": auth_cookie_info})
    return access_token


def validate_one_time_token(request):
    pass


def set_auth_cookie(response, access_token):
    IS_PRODUCTION = deployment == "cloud"
    max_age = 30 * 24 * 60 * 60  # 30 days

    server_domain = (
        "localhost"
        if deployment == "local"
        else os.environ.get("REACT_APP_SERVER_APP_URL")
    )
    if deployment == "cloud":
        server_domain = server_domain[len("https://") :]
    auth_cookie_info = {
        "name": "auth_cookie",
        "value": access_token,
        "max_age": max_age,
        "httponly": True,
        "secure": IS_PRODUCTION,
        "samesite": "None" if IS_PRODUCTION else "Lax",
        "path": "/",
        "domain": server_domain,
    }

    # Attach the info to payload for React to set
    attach_data_to_payload(response, {"auth_cookie_info": auth_cookie_info})
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
