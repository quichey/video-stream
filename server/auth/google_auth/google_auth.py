from authlib.integrations.flask_client import OAuth

from auth.ThirdPartyAuth import ThirdPartyAuth


class GoogleAuth(ThirdPartyAuth):
    PROVIDER = "google"
    GOOGLE_CLIENT_ID = ""
    GOOGLE_CLIENT_SECRET = ""

    def __init__(self, app, deployment, *args, **kwargs):
        super().__init__(deployment, args, **kwargs)
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

    def authorize(self):
        token = self.oauth_client.authorize_access_token()
        resp = self.oauth_client.get("userinfo")
        user_info = resp.json()
        return {
            "token": token,
            user_info: user_info,
        }

    def get_authorize_url(self, redirect_uri):
        # Returns the URL to redirect the user for Google OAuth
        return self.oauth_client.authorize_redirect(redirect_uri)
