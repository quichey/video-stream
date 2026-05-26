import shutil
import os
from dotenv import load_dotenv

# Path to the Chrome profile you created manually
SELENIUM_PROFILE_PATH = "profiles/selenium_profile_folder"

# Optional: you can add other profile-specific options here
HEADLESS = True  # whether to run tests headless
WINDOW_SIZE = "1920,1080"

load_dotenv()


def borrow_creds():
    SOURCE_PROFILE = os.environ.get("SOURCE_PROFILE")
    DEST_PROFILE = r"./profiles/selenium_profile_folder"
    # Remove old test profile
    if os.path.exists(DEST_PROFILE):
        shutil.rmtree(DEST_PROFILE)

    # Copy essential files/folders
    shutil.copytree(
        SOURCE_PROFILE,
        DEST_PROFILE,
        ignore=shutil.ignore_patterns(
            "LOCK", "Sessions", "Sync Data", "GPUCache", "Cache"
        ),
    )
