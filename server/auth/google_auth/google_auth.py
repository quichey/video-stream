from typing_extensions import override
import os
from authlib.integrations.flask_client import OAuth

from auth.ThirdPartyAuth import ThirdPartyAuth, Cred
from util.deployment import Deployment

deployment_class = Deployment()
print(f"\n\n deployment_class.deployment: {deployment_class.deployment} \n\n")
if deployment_class.deployment == "local":
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
elif deployment_class.deployment == "cloud":
    print(
        f"\n\n deployment_class.deployment_env: {deployment_class.deployment_env} \n\n"
    )
    GOOGLE_CLIENT_ID = os.environ.get(
        f"{deployment_class.deployment_env.upper()}_GOOGLE_CLIENT_ID"
    )
    GOOGLE_CLIENT_SECRET = os.environ.get(
        f"{deployment_class.deployment_env.upper()}_GOOGLE_CLIENT_SECRET"
    )


class GoogleAuth(ThirdPartyAuth):
    PROVIDER = "google"
    GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET = GOOGLE_CLIENT_SECRET

    def init_app(self, app):
        print(f"\n\n self.GOOGLE_CLIENT_ID: {self.GOOGLE_CLIENT_ID} \n\n")
        print(f"\n\n self.GOOGLE_CLIENT_SECRET: {self.GOOGLE_CLIENT_SECRET} \n\n")
        self.oauth = OAuth(app)
        self.oauth_client = self.oauth.register(
            name="google",
            client_id=self.GOOGLE_CLIENT_ID,
            client_secret=self.GOOGLE_CLIENT_SECRET,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )
        return

    @override
    def get_authorize_url(self, redirect_uri):
        # Returns the URL to redirect the user for Google OAuth
        return self.oauth_client.authorize_redirect(redirect_uri)

    @override
    def _extract_authorizor_creds(self, request, response) -> Cred:
        # Exchange 'code' from query params for an access token
        token = self.oauth_client.authorize_access_token()

        userinfo_endpoint = self.oauth_client.server_metadata["userinfo_endpoint"]
        # Use the token to get user info
        resp = self.oauth_client.get(userinfo_endpoint)
        user_info = resp.json()

        # Example: user_info contains 'email', 'name', 'picture', etc.
        return Cred(
            provider_user_id=user_info["sub"],
            access_token=token["access_token"],
            expires_at=token["expires_at"],
            email=user_info["email"],
        )


GOOGLE_AUTH = GoogleAuth()
