from typing import override
from authlib.integrations.flask_client import OAuth

from auth.ThirdPartyAuth import ThirdPartyAuth


class GoogleAuth(ThirdPartyAuth):
    PROVIDER = "google"
    GOOGLE_CLIENT_ID = ""
    GOOGLE_CLIENT_SECRET = ""

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

    @override
    def authorize(self):
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
    def extract_authorizor_creds(self, request, response):
        # Exchange 'code' from query params for an access token
        token = self.oauth_client.authorize_access_token()

        # Use the token to get user info
        resp = self.oauth_client.get("userinfo")
        user_info = resp.json()

        # Example: user_info contains 'email', 'name', 'picture', etc.
        return {
            "user_info": user_info,
            "token": token,
        }

    @override
    def get_user_id(self, creds):
        pass

    @override
    def get_provider_user_id(self, creds):
        pass

    @override
    def get_access_token(self, creds):
        pass

    @override
    def get_metadata(self, creds):
        pass


GOOGLE_AUTH = GoogleAuth()
