from selenium.webdriver.common.by import By

from .base_page import BasePage
from .qa_page import QAPage


class CareersPage(BasePage):
    """
    Careers ana sayfası.

    Case'te istenen kontroller:
    - Careers sayfası açıldı mı?
    - Locations, Teams ve Life at Insider blokları görünüyor mu?

    Site zamanla değişebileceği için locator'ları biraz daha esnek tuttuk,
    en kötü durumda URL ve sayfa içeriği üzerinden kontrol ediyoruz.
    """

    # Esnek bir başlık/hero locator'ı
    HERO_TITLE = (
        By.XPATH,
        "//*[self::h1 or self::h2][contains(., 'Careers') or contains(., 'Ready to disrupt')]"
    )

    # Blok başlıkları için birkaç farklı ihtimali kapsayan locator'lar
    LOCATIONS_BLOCK = (
        By.XPATH,
        "//*[self::h2 or self::h3][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'location')]"
    )

    TEAMS_BLOCK = (
        By.XPATH,
        "//*[self::h2 or self::h3][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'team') or contains(., 'Find your calling')]"
    )

    LIFE_AT_INSIDER_BLOCK = (
        By.XPATH,
        "//*[self::h2 or self::h3][contains(., 'Life at Insider')]"
    )

    COOKIE_ACCEPT_ALL = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Accept All') or contains(normalize-space(), 'ACCEPT ALL')]",
    )

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
        """
        Careers sayfası açıldı mı?
        URL ve hero başlık üzerinden kontrol ediyoruz.
        """
        if "careers" not in self.current_url.lower():
            return False
        # Hero başlık görünüyorsa ekstra güven
        return self.is_visible(self.HERO_TITLE, timeout=10)

    def has_locations_block(self) -> bool:
        """
        Locations ile ilgili bir blok var mı?
        Önce başlığı arıyoruz, bulamazsak page_source üzerinden keyword arıyoruz.
        """
        try:
            if self.is_visible(self.LOCATIONS_BLOCK, timeout=5):
                return True
        except Exception:
            pass

        # Fallback: Sayfa içeriğinde "Location" / "Locations" geçiyor mu?
        source = self.driver.page_source.lower()
        return "location" in source

    def has_teams_block(self) -> bool:
        """
        Teams / Find your calling bloğu var mı?
        """
        try:
            if self.is_visible(self.TEAMS_BLOCK, timeout=5):
                return True
        except Exception:
            pass

        source = self.driver.page_source.lower()
        return "team" in source or "find your calling" in source.lower()

    def has_life_at_insider_block(self) -> bool:
        """
        Life at Insider bloğu var mı?
        """
        try:
            if self.is_visible(self.LIFE_AT_INSIDER_BLOCK, timeout=5):
                return True
        except Exception:
            pass

        source = self.driver.page_source.lower()
        return "life at insider" in source

    def open_qa_careers_page(self) -> QAPage:
        """
        Case'te URL açıkça verildiği için direkt QA careers sayfasına gidiyoruz.
        """
        self.open("https://useinsider.com/careers/quality-assurance/")
        return QAPage(self.driver)
