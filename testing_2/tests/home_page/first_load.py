# testing_2/tests/test_first_load.py

from drivers.driver import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FirstLoad:
    BASE_URL = "http://localhost:3000"  # Replace with deployed URL if needed

    def __init__(self):
        self.wait = WebDriverWait(driver, 10)

    def load_home_page(self):
        driver.get(self.BASE_URL)
        # Check page header/title contains 'Search'
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Search')]"))
        )

    def load_videos(self):
        # Wait for the video list to appear
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="home-videos-list"]')
            )
        )

        # Ensure at least one video thumbnail is loaded
        videos = driver.find_elements(
            By.CSS_SELECTOR, '[data-testid="home-video-list-item"]'
        )
        assert len(videos) > 0, "Expected at least one video in the list"

    def navigate_to_watch_video(self, video_index=0):
        # Click on the first video (or specified index)
        videos = driver.find_elements(
            By.CSS_SELECTOR, '[data-testid="home-video-list-item"]'
        )
        videos[video_index].click()

        # Wait for video player to appear
        video_el = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="video-player"]')
            )
        )

        # Check that video duration is greater than 0
        video_tag = driver.find_element(
            By.CSS_SELECTOR, 'video[data-testid="video-player"]'
        )
        duration = driver.execute_script("return arguments[0].duration;", video_tag)
        assert duration > 0, f"Expected video duration > 0, got {duration}"

    def run_suite(self):
        self.load_home_page()
        self.load_videos()
        self.navigate_to_watch_video()
