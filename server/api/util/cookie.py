import uuid


def generate_uuid():
    _uuid = str(uuid.uuid4())
    return _uuid

def generate_cookie(name, deployment, response):
    cookie_id = generate_uuid()
    IS_PRODUCTION = deployment is 'cloud'
    response.set_cookie(
        name,
        cookie_id,
        max_age=30*24*60*60,  # 30 days
        httponly=True,
        secure=IS_PRODUCTION,  # True in production (HTTPS), False locally
        samesite='None' if IS_PRODUCTION else 'Lax',  # None for cross-site in prod, Lax for local
        path='/'
    )
    return cookie_id

def expire_cookie(name, deployment, response):
    response.set_cookie(name,
        value="",
        expires=0,       # Expire immediately
        path="/",
        httponly=True,
        secure=True,
        samesite="Strict"
    )
    return
