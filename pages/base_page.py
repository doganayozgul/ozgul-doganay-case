from typing import List, Optional, Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def click(self, locator: Tuple[str, str]) -> WebElement:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def find(self, locator: Tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: Tuple[str, str]) -> List[WebElement]:
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def is_visible(
        self, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> bool:
        try:
            if timeout:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
            else:
                self.find(locator)
            return True
        except TimeoutException:
            return False

    def scroll_into_view(self, element: WebElement) -> None:
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            element,
        )

    @property
    def current_url(self) -> str:
        return self.driver.current_url
