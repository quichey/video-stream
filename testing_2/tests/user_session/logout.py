# testing_2/tests/test_logout.py

from drivers.driver import driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


class LogOut:
    def log_out(self):
        # Click logout menu item
        driver.find_element(By.CSS_SELECTOR, '[data-testid="logout-menu-item"]').click()

        # TODO: replace time.sleep with WebDriverWait for robustness
        time.sleep(2)

        # Verify that view-channel-menu-item no longer exists
        try:
            driver.find_element(
                By.CSS_SELECTOR, '[data-testid="view-channel-menu-item"]'
            )
            assert False, "view-channel-menu-item should not exist after logout"
        except NoSuchElementException:
            # ✅ expected behavior: element not found
            pass

    def run_suite(self):
        self.log_out()
