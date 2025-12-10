from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://insiderone.com/"

    COOKIE_ACCEPT_ALL = (
        By.XPATH,
        (
            "//button[contains(normalize-space(), 'Accept All') "
            "or contains(normalize-space(), 'ACCEPT ALL')] | "
            "//*[@role='button' and (contains(normalize-space(), 'Accept All') "
            "or contains(normalize-space(), 'ACCEPT ALL'))]"
        ),
    )

    def open_home(self) -> None:
        self.open(self.URL)

    def accept_cookies_if_present(self) -> None:
        try:
            if self.is_visible(self.COOKIE_ACCEPT_ALL, timeout=5):
                self.click(self.COOKIE_ACCEPT_ALL)
        except TimeoutException:
            pass

    def is_loaded(self) -> bool:
        return "Insider" in self.driver.title
