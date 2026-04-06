# testing_2/tests/test_login.py

from drivers.driver import driver
from selenium.webdriver.common.by import By
import time


class LoginTests:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def open_dialog(self):
        # Click login menu item
        driver.find_element(By.CSS_SELECTOR, '[data-testid="login-menu-item"]').click()

        # Wait until login dialog is visible
        dialog = driver.find_element(By.CSS_SELECTOR, '[data-testid="login-dialogue"]')
        assert dialog.is_displayed(), "Login dialog should be visible"

    def submit(self):
        # Fill username
        name_field = driver.find_element(By.CSS_SELECTOR, '[data-testid="login-name"]')
        name_field.clear()
        name_field.send_keys(self.username)

        # Fill password
        pwd_field = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="login-password"]'
        )
        pwd_field.clear()
        pwd_field.send_keys(self.password)

        # Click submit
        driver.find_element(By.CSS_SELECTOR, '[data-testid="login-submit"]').click()

        # TODO: replace time.sleep with WebDriverWait for robustness
        time.sleep(2)

        # Assert user’s name is visible
        channel_menu = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="view-channel-menu-item"]'
        )
        assert channel_menu.is_displayed()
        assert self.username in channel_menu.text

    def run_suite(self):
        self.open_dialog()
        self.submit()
