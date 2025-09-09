from typing import override
import os
from authlib.integrations.flask_client import OAuth

from auth.ThirdPartyAuth import ThirdPartyAuth, Cred


class GoogleAuth(ThirdPartyAuth):
    PROVIDER = "google"
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

    def init_app(self, app):
        self.oauth = OAuth(app)
        self.oauth_client = self.oauth.register(
            name="google",
            client_id=self.GOOGLE_CLIENT_ID,
            client_secret=self.GOOGLE_CLIENT_SECRET,
            access_token_url="https://accounts.google.com/o/oauth2/token",
            authorize_url="https://accounts.google.com/o/oauth2/auth",
            api_base_url="https://www.googleapis.com/oauth2/v1/",
            client_kwargs={"scope": "openid email profile"},
        )
        return

    # TODO: don't need this?
    # previously was @override: authorize
    def g_authorize(self):
        token = self.oauth_client.authorize_access_token()
        resp = self.oauth_client.get("userinfo")
        user_info = resp.json()
        return {
            "token": token,
            user_info: user_info,
        }

    @override
    def get_authorize_url(self, redirect_uri):
        # Returns the URL to redirect the user for Google OAuth
        return self.oauth_client.authorize_redirect(redirect_uri)

    @override
    def _extract_authorizor_creds(self, request, response) -> Cred:
        # Exchange 'code' from query params for an access token
        token = self.oauth_client.authorize_access_token()

        # Use the token to get user info
        resp = self.oauth_client.get("userinfo")
        user_info = resp.json()

        # Example: user_info contains 'email', 'name', 'picture', etc.
        return Cred(
            provider_user_id=user_info["id"],
            access_token=token["access_token"],
            email=user_info["email"],
        )


GOOGLE_AUTH = GoogleAuth()
