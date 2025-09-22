# testing_2/tests/test_session_menu.py

from drivers.driver import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SessionMenu:
    def __init__(self):
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        # Click on session menu button
        driver.find_element(By.CSS_SELECTOR, '[data-testid="session-menu-btn"]').click()

        # Wait until popover is visible
        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="session-menu-popover"]')
            )
        )

    def run_suite(self):
        self.open()
