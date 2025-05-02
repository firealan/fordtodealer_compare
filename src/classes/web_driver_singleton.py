# 3rd Party Pacakges
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
import logging

# Built-in Packages
import os
import time

# Local Packages
from utilities.constants import constants as const

# Load environment variables from the .env file
load_dotenv(override=True)


class WebDriverSingleton:
    _driver = None
    _retry_count = 0
    _max_retries = 3
    _driver_type = None

    @classmethod
    def get_driver(cls):
        cls._driver_type = (
            const["BROWSER_DRIVER_TYPE"].lower()
            if cls._driver_type is None
            else cls._driver_type
        )

        # Check if driver exists and is still valid
        if cls._driver is not None:
            try:
                # A simple check to see if the session is still active
                # Just getting the window handles is a lightweight operation
                cls._driver.window_handles
            except (WebDriverException, InvalidSessionIdException) as e:
                logging.warning(f"WebDriver session is no longer valid: {str(e)}")
                logging.info("Recreating WebDriver session...")
                cls._driver = None
                cls._retry_count += 1

        # Create a new driver if needed
        if cls._driver is None:
            driver_type = cls._driver_type

            if driver_type == "chrome":
                cls._driver = cls.setup_chrome_driver()
            elif driver_type == "firefox":
                cls._driver = cls.setup_firefox_driver()
            elif driver_type == "edge":
                cls._driver = cls.setup_edge_driver()
            else:
                raise ValueError(
                    "Invalid BROWSER_DRIVER_TYPE in the constants.py file. Use 'chrome', 'firefox', or 'edge'."
                )

            # Reset retry count after successful creation
            if cls._driver is not None:
                cls._retry_count = 0

        return cls._driver

    @staticmethod
    def setup_chrome_driver():
        chrome_service = ChromeService(ChromeDriverManager().install())
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option("detach", False)
        headless_mode = const["HEADLESS_MODE"]
        if headless_mode:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        return driver

    @staticmethod
    def setup_edge_driver():
        edge_service = EdgeService(EdgeChromiumDriverManager().install())
        edge_options = EdgeOptions()
        edge_options.add_experimental_option("detach", False)
        headless_mode = const["HEADLESS_MODE"]
        if headless_mode:
            edge_options.add_argument("--headless")
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Edge(service=edge_service, options=edge_options)
        return driver

    @staticmethod
    def setup_firefox_driver():
        os.environ["GH_TOKEN"] = os.getenv("GITHUB_TOKEN")
        firefox_service = FirefoxService(GeckoDriverManager().install())
        firefox_options = FirefoxOptions()

        # Add options for better stability in containerized environments
        firefox_options.add_argument("--disable-gpu")
        headless_mode = const["HEADLESS_MODE"]
        if headless_mode:
            firefox_options.add_argument("--headless")

        # Add Firefox-specific options for container environment
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.set_preference("browser.tabs.remote.autostart", False)
        firefox_options.set_preference("browser.tabs.remote.autostart.1", False)
        firefox_options.set_preference("browser.tabs.remote.autostart.2", False)

        # More memory settings that can help stability
        firefox_options.add_argument("--disable-extensions")
        firefox_options.add_argument("--disable-application-cache")
        firefox_options.add_argument("--disable-infobars")

        try:
            driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
            driver.set_window_size(1920, 1080)
            # Set page load timeout to prevent long hangs
            driver.set_page_load_timeout(60)
            driver.set_script_timeout(30)
            return driver
        except Exception as e:
            logging.error(f"Failed to initialize Firefox WebDriver: {str(e)}")
            # If Firefox fails, we could try with a fallback browser
            raise
