from google.google_auth import GoogleAuth

# Map provider names to classes
auth_providers = {
    "google": GoogleAuth,
    # "facebook": FacebookAuth,
}


def get_auth(provider_name):
    cls = auth_providers.get(provider_name)
    if cls is None:
        raise ValueError(f"No auth provider registered for {provider_name}")
    return cls()
