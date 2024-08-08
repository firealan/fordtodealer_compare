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

# Built-in Packages
import os

# Local Packages
from utilities.constants import constants as const

# Load environment variables from the .env file
load_dotenv(override=True)


class WebDriverSingleton:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            driver_type = const["BROWSER_DRIVER_TYPE"].lower()

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
        driver = webdriver.Edge(service=edge_service, options=edge_options)
        return driver

    @staticmethod
    def setup_firefox_driver():
        os.environ["GH_TOKEN"] = os.getenv("GITHUB_TOKEN")
        firefox_service = FirefoxService(GeckoDriverManager().install())
        firefox_options = FirefoxOptions()
        firefox_options.add_argument(
            "--disable-gpu"
        )  # Add any additional options if needed
        headless_mode = const["HEADLESS_MODE"]
        if headless_mode:
            firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
        driver.set_window_size(1920, 1080)
        return driver
