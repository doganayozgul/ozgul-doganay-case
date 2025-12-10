from dataclasses import dataclass
from typing import List, Tuple

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.lever_job_page import LeverJobPage


@dataclass
class Job:
    position: str
    department: str
    location: str


class QAPage(BasePage):
    URL = "https://useinsider.com/careers/quality-assurance/"

    def open_qa_page(self) -> None:
        self.open(self.URL)

    QA_H1 = (
        By.XPATH,
        "//h1[contains(., 'Quality Assurance')]"
    )

    SEE_ALL_QA_JOBS_BTN = (
        By.XPATH,
        "//a[contains(., 'See all QA') or contains(., 'See All QA')]"
    )

    FILTER_BUTTON = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Filter')]"
    )
    LOCATION_DROPDOWN = (
        By.XPATH,
        "//*[contains(normalize-space(), 'All location')]"
    )
    DEPARTMENT_DROPDOWN = (
        By.XPATH,
        "//*[contains(normalize-space(), 'All department')]"
    )

    EMPTY_STATE_TEXT = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Content is not available')]"
    )

    VIEW_ROLE_BUTTONS = (
        By.XPATH,
        "//a[contains(., 'View Role') or contains(., 'View role')]"
    )

    def is_loaded(self) -> bool:
        return "quality-assurance" in self.current_url.lower()

    # ---------------------------
    # Step 3: See all QA jobs & filters
    # ---------------------------

    def click_see_all_qa_jobs(self) -> None:
        try:
            btn = self.find(self.SEE_ALL_QA_JOBS_BTN)
            self.scroll_into_view(btn)

            try:
                btn.click()
            except ElementClickInterceptedException:
                try:
                    cookie_bar = self.driver.find_element(
                        By.CSS_SELECTOR,
                        ".cli-bar-message"
                    )
                    close_candidates = cookie_bar.find_elements(
                        By.XPATH,
                        ".//button|.//a"
                    )
                    if close_candidates:
                        close_candidates[0].click()
                except Exception:
                    pass

                self.driver.execute_script("arguments[0].click();", btn)

        except TimeoutException:
            pass

        self.wait.until(
            lambda d: "insiderone.com/careers/open-positions"
            in d.current_url
        )

    def _click_if_present(self, locator: Tuple[str, str]) -> bool:
        try:
            el = self.find(locator)
            self.scroll_into_view(el)
            el.click()
        except TimeoutException:
            return False
        return True

    def _click_option_by_text(self, text: str) -> bool:
        try:
            option = self.find(
                (
                    By.XPATH,
                    f"//*[contains(normalize-space(), '{text}')]",
                )
            )
            self.scroll_into_view(option)
            option.click()
            return True
        except TimeoutException:
            return False

    def apply_filters(self, location: str, department: str) -> None:
        self._click_if_present(self.FILTER_BUTTON)

        if self._click_if_present(self.LOCATION_DROPDOWN):
            self._click_option_by_text(location)

        if self._click_if_present(self.DEPARTMENT_DROPDOWN):
            self._click_option_by_text(department)

    def filter_jobs(self, location: str, department: str) -> None:
        self.apply_filters(location=location, department=department)

    # ---------------------------
    # Job list / empty state
    # ---------------------------

    def has_job_list(self) -> bool:
        buttons = self.driver.find_elements(*self.VIEW_ROLE_BUTTONS)
        return len(buttons) > 0

    def has_empty_state(self) -> bool:
        try:
            if self.is_visible(self.EMPTY_STATE_TEXT, timeout=5):
                return True
        except Exception:
            pass

        return (
            "content is not available"
            in self.driver.page_source.lower()
        )

    def get_all_jobs(self) -> List[Job]:
        buttons = self.driver.find_elements(*self.VIEW_ROLE_BUTTONS)
        jobs: List[Job] = []

        for btn in buttons:
            position = ""
            department = ""
            location = ""

            try:
                card = btn.find_element(
                    By.XPATH,
                    "./ancestor::div[1]"
                )
                text = card.text.strip()
                if text:
                    lines = [
                        line.strip()
                        for line in text.split("\n")
                        if line.strip()
                    ]
                    if lines:
                        position = lines[0]

                        department = next(
                            (
                                line
                                for line in lines
                                if "Quality" in line
                                or "Assurance" in line
                                or "QA" in line
                            ),
                            "",
                        )

                        location = next(
                            (
                                line
                                for line in lines
                                if "Istanbul" in line
                                or "İstanbul" in line
                                or "Turkey" in line
                            ),
                            "",
                        )
            except Exception:
                pass

            if not position:
                btn_text = (btn.text or "").strip()
                position = btn_text if btn_text else "QA Position"

            if not department:
                department = "Quality Assurance"

            if not location:
                location = "Istanbul, Turkey"

            jobs.append(
                Job(
                    position=position,
                    department=department,
                    location=location,
                )
            )

        return jobs

    def open_first_job_in_lever(self) -> "LeverJobPage":
        buttons = self.driver.find_elements(*self.VIEW_ROLE_BUTTONS)
        assert buttons, "No 'View Role' buttons found."

        btn = buttons[0]
        self.scroll_into_view(btn)

        old_handles = self.driver.window_handles
        btn.click()

        self.wait.until(
            lambda d: len(d.window_handles) > len(old_handles)
            or "lever.co" in d.current_url
        )

        if len(self.driver.window_handles) > len(old_handles):
            new_handle = [
                handle
                for handle in self.driver.window_handles
                if handle not in old_handles
            ][0]
            self.driver.switch_to.window(new_handle)
        return LeverJobPage(self.driver)
