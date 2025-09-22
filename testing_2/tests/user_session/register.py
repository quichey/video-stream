# testing_2/tests/test_register.py

from drivers.driver import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegisterTests:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.wait = WebDriverWait(driver, 10)

    def open_dialog(self):
        # Click on register menu item
        driver.find_element(
            By.CSS_SELECTOR, '[data-testid="register-menu-item"]'
        ).click()

        # Wait for the dialog to become visible
        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="register-dialogue"]')
            )
        )

    def submit(self):
        # Fill in username and password
        driver.find_element(By.CSS_SELECTOR, '[data-testid="register-name"]').send_keys(
            self.username
        )
        driver.find_element(
            By.CSS_SELECTOR, '[data-testid="register-password"]'
        ).send_keys(self.password)

        # Submit form
        driver.find_element(By.CSS_SELECTOR, '[data-testid="register-submit"]').click()

        # Wait for channel menu item to be visible and contain the username
        el = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="view-channel-menu-item"]')
            )
        )
        assert self.username in el.text, (
            f"Expected username '{self.username}' in channel menu, got '{el.text}'"
        )

    def run_suite(self):
        self.open_dialog()
        self.submit()
