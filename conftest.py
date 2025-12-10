import pytest
from typing import Generator

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver

from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver() -> Generator[WebDriver, None, None]:
    """Create and yield a Chrome WebDriver instance for testing."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )
    driver.implicitly_wait(5)

    yield driver

    driver.quit()
