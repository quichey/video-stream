from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver(profile_path=None, headless=True):
    chrome_options = Options()
    if profile_path:
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)


driver = create_driver(profile_path="profiles/selenium_profile")
