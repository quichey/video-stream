import os

def detect_environment():
    """Detect if running in cloud shell vs local."""
    if os.environ.get("CLOUD_SHELL", "") == "true":
        return "cloud"
    return "local"
