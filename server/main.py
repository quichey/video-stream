import os

from api import create_app


if __name__ == "__main__":
    app = create_app()
    # Cloud Run provides the port in an environment variable called PORT
    port = int(os.environ.get("PORT", 8080))
    # Binding to 0.0.0.0 is mandatory for Cloud Run
    app.run(host="0.0.0.0", port=8080)