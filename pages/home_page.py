from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage

class HomePage(BasePage):
    URL = "https://insiderone.com/"

    COOKIE_ACCEPT_ALL = (
        By.XPATH,
        "//button[contains(normalize-space(), 'Accept All') or contains(normalize-space(), 'ACCEPT ALL')] | //*[@role='button' and (contains(normalize-space(), 'Accept All') or contains(normalize-space(), 'ACCEPT ALL'))]",
    )

    def open_home(self) -> None:
        """Open the home page."""
        self.open(self.URL)

    def accept_cookies_if_present(self) -> None:
        """Accept cookies if cookie banner is present."""
        try:
            # Wait for cookie banner to be visible with a shorter timeout
            if self.is_visible(self.COOKIE_ACCEPT_ALL, timeout=5):
                # Use BasePage's click method which includes explicit wait and clickability check
                self.click(self.COOKIE_ACCEPT_ALL)
        except TimeoutException:
            # Cookie banner is not present, which is fine
            pass

    def is_loaded(self) -> bool:
        """Check if the home page is loaded."""
        return "Insider" in self.driver.title
