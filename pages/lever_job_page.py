# pages/lever_job_page.py
from selenium.webdriver.common.by import By

from .base_page import BasePage


class LeverJobPage(BasePage):
    # Çok detaylı bir POM'e ihtiyaç yok; sadece doğru domaine yönlendik mi bakıyoruz
    LEVER_LOGO_OR_HEADER = (
        By.XPATH,
        "//*[contains(@class, 'posting-header') or contains(., 'Apply for this job')]"
    )

    def is_loaded(self) -> bool:
        """
        Check that we are on Lever Application form page.
        - URL 'lever.co' içeriyor mu?
        - Başvuru header'ı vb. görünüyor mu?
        """
        url_ok = "lever.co" in self.current_url
        # Bazı durumlarda sadece URL check de yeterli olabilir, ama en azından bir element arayalım
        try:
            element_ok = self.is_visible(self.LEVER_LOGO_OR_HEADER, timeout=15)
        except Exception:
            element_ok = False

        return url_ok and element_ok
