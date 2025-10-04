import os
from dotenv import load_dotenv
from pathlib import Path

# --- Configuration Loading ---

# Define the absolute path to the .env file.
# This assumes settings.py is in the 'server' directory and the .env file
# should be located one directory deeper in 'server/db/.env'.
# Path(__file__).resolve().parent gives the directory containing this file (e.g., /path/to/server)
ENV_FILE_PATH = Path(__file__).resolve().parent / "db" / ".env"

# Load environment variables from the specific path.
# load_dotenv() is called with the explicit path for robustness.
load_dotenv(dotenv_path=ENV_FILE_PATH)

# --- Configuration Constants ---

# The URL prefix for the Google Auth API or the service endpoint
GOOGLE_AUTH_URL = os.getenv(
    "GOOGLE_AUTH_URL", "https://accounts.google.com/o/oauth2/auth"
)

# Client ID and Secret for the Google application
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# The redirect URI must match what is configured in the Google API Console
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# Ensure critical variables are set (Fail fast principle)
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    # Use print instead of raising an error directly if this file is imported early,
    # allowing the app to potentially run checks later, but still warning the developer.
    # Note: Check if the .env file exists and print a more descriptive warning if not.
    if not ENV_FILE_PATH.exists():
        print(
            f"⚠️ FATAL WARNING: .env file not found at expected location: {ENV_FILE_PATH}"
        )
    else:
        print(
            "⚠️ WARNING: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET environment variables are set to None. Check .env content."
        )


def get_google_config():
    """
    Returns a dictionary of Google configuration details.
    This is the only function other parts of the application should import and use.
    """
    return {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_url": GOOGLE_AUTH_URL,
        "redirect_uri": GOOGLE_REDIRECT_URI,
    }


# Example usage within this file:
# if __name__ == "__main__":
#     config = get_google_config()
#     print(f"Loaded Client ID: {config['client_id']}")
#     print(f"Loaded Secret: {'(SET)' if config['client_secret'] else '(NOT SET)'}")
