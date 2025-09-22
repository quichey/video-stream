from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from profiles.selenium_profile import (
    SELENIUM_PROFILE_PATH,
    HEADLESS,
    WINDOW_SIZE,
    borrow_creds,
)


def create_driver():
    borrow_creds()
    chrome_options = Options()
    if SELENIUM_PROFILE_PATH:
        chrome_options.add_argument(f"--user-data-dir={SELENIUM_PROFILE_PATH}")
    if HEADLESS:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
    return webdriver.Chrome(options=chrome_options)


driver = create_driver()
