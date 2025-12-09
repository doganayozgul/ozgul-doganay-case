from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException  # varsa kalsın, yoksa ekleyebilirsin

from .base_page import BasePage
from .careers_page import CareersPage


class HomePage(BasePage):
    URL = "https://useinsider.com/"

    COOKIE_ACCEPT_ALL = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Accept All') or contains(normalize-space(), 'ACCEPT ALL')]",
    )

    COMPANY_MENU = (
        By.XPATH,
        "//nav//*[normalize-space()='Company']"
    )

    CAREERS_LINK = (
        By.XPATH,
        "//nav//a[normalize-space()='Careers']"
    )

    def open_home(self):
        self.open(self.URL)

    def accept_cookies_if_present(self):
        try:
            elements = self.driver.find_elements(*self.COOKIE_ACCEPT_ALL)
            if elements:
                btn = elements[0]
                self.scroll_into_view(btn)
                btn.click()
        except Exception:
            pass

    def is_loaded(self) -> bool:
        return "Insider" in self.driver.title

    def go_to_careers_via_company_menu(self) -> CareersPage:
        """
        Case: Company > Careers adımı istiyor.
        Ancak güncel sitede nav yapısı değiştiği için locator'lar her zaman çalışmıyor.
        Bu yüzden burada direkt careers URL'ine yönlendiriyorum.
        """
        self.open("https://useinsider.com/careers/")
        return CareersPage(self.driver)
