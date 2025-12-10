from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LeverJobPage(BasePage):
    LEVER_LOGO_OR_HEADER = (
        By.XPATH,
        (
            "//*[contains(@class, 'posting-header') "
            "or contains(., 'Apply for this job')]"
        ),
    )

    def is_loaded(self) -> bool:
        url_ok = "lever.co" in self.current_url
        try:
            element_ok = self.is_visible(
                self.LEVER_LOGO_OR_HEADER, timeout=15
            )
        except Exception:
            element_ok = False

        return url_ok and element_ok
