import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask on Cloud Run is working!"

if __name__ == "__main__":
    # Cloud Run provides the port in an environment variable called PORT
    port = int(os.environ.get("PORT", 8080))
    # Binding to 0.0.0.0 is mandatory for Cloud Run
    app.run(host="0.0.0.0", port=port)