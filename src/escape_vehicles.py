# 3rd Party Pacakges
from dotenv import load_dotenv
import pandas as pd
from selenium.webdriver.common.by import By

# Built-in Packages
import time
from typing import List, Tuple
import os
import sys

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(script_dir))
sys.path.append(os.path.join(os.path.dirname(script_dir), "src"))

# Local Packages
from utilities.constants import constants as const
from utilities.utilities import parse_img_filename
from classes.web_driver_singleton import WebDriverSingleton

# Load environment variables from the .env file
load_dotenv(override=True)


# ------------------------------------------
# Get prices from ford.ca
# ------------------------------------------
def get_ford_mfg_escape_prices(url: str) -> List[Tuple[str, str]]:

    # Set up the Web driver
    driver = WebDriverSingleton.get_driver()

    # Vehicle URL
    driver.get(url)
    time.sleep(const["TIME_SLEEP"])  # Allow time for the page to load

    vehicle_prices = []

    try:
        # Extract vehicle models and prices
        model_elements = driver.find_elements(
            By.XPATH, "//*[@class='bri-txt generic-title-one ff-b']"
        )
        price_elements = driver.find_elements(
            By.XPATH, '//*[@class="bri-txt body-one ff-b"]'
        )

        # Check if model or price elements are not found
        if not model_elements or not price_elements:
            raise Exception(
                "Model or price elements not found. Page structure may have changed."
            )

        for model, price in zip(model_elements, price_elements):
            model_name = model.text.strip()
            price_value = price.text.strip()
            if model_name == "" or price_value == "":
                continue
            vehicle_prices.append((model_name, price_value))

    except Exception as e:
        vehicle_prices = [("Ford.ca Error", str(e))]

    return vehicle_prices


# ------------------------------------------
# Get prices from fordtodealers.ca
# ------------------------------------------
def get_ford_dealer_escape_prices(url: str) -> List[Tuple[str, str]]:

    # Set up the Web driver
    driver = WebDriverSingleton.get_driver()

    # Vehicle URL
    driver.get(url)
    time.sleep(const["TIME_SLEEP"])  # Allow time for the page to load

    vehicle_prices = []

    try:
        # Extract vehicle models and prices
        model_elements = driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'modelChecker')]/div/ul/li/a/span",
        )

        price_elements = driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'modelChecker')]/div/ul/li/a/span/label",
        )

        # Check if model or price elements are not found
        if not model_elements or not price_elements:
            raise Exception(
                "Model or price elements not found. Page structure may have changed."
            )

        for model, price in zip(model_elements, price_elements):
            model_name = model.text.strip().split("\n")[
                0
            ]  # Strip everything after '\n'
            price_value = price.text.strip()
            if model_name == "" or price_value == "":
                continue
            vehicle_prices.append((model_name, price_value))

    except Exception as e:
        vehicle_prices = [("Fordtodealers.ca Error", str(e))]

    return vehicle_prices


# ------------------------------------------
# Get hero image from ford.ca
# ------------------------------------------
def get_ford_mfg_escape_hero_img(url: str) -> str:

    # Set up the Web driver
    driver = WebDriverSingleton.get_driver()

    # Vehicle URL
    driver.get(url)
    time.sleep(const["TIME_SLEEP"])  # Allow time for the page to load

    vehicle_image = ""

    try:
        # Find the img tag using a more general XPath
        img_element = driver.find_element(
            By.XPATH, '//div[@class="billboard-img"]//picture/img'
        )
        img_src = img_element.get_attribute("src")

        # Extract the part of the URL containing image using regular expressions
        match = parse_img_filename(img_src=img_src)

        if match:
            # Get the matched group (filename with image file extension)
            vehicle_image = match.group(1)

        else:
            vehicle_image = "No image filename found"

    except Exception as e:
        vehicle_image = str(e)

    return vehicle_image


# ------------------------------------------
# Get hero image from fordtodealers.ca
# ------------------------------------------
def get_ford_dealer_escape_hero_img(url: str) -> str:

    # Set up the Web driver
    driver = WebDriverSingleton.get_driver()

    # Vehicle URL
    driver.get(url)
    time.sleep(const["TIME_SLEEP"])  # Allow time for the page to load

    vehicle_image = ""

    try:
        # Find the img tag using a more general XPath
        img_element = driver.find_element(
            By.XPATH,
            '//div[starts-with(@class,"row-bg") and contains(@class,"using-image")]',
        )
        img_src = img_element.get_attribute("style")

        # Extract the part of the URL containing image using regular expressions
        match = parse_img_filename(img_src=img_src)

        if match:
            # Get the matched group (filename with image file extension)
            vehicle_image = match.group(1)

        else:
            vehicle_image = "No image filename found"

    except Exception as e:
        vehicle_image = str(e)

    return vehicle_image


# Test Functions
if __name__ == "__main__":
    print(get_ford_mfg_escape_prices(const["ESCAPE_MANUFACTURER_URL"]))
    print(get_ford_dealer_escape_prices(const["ESCAPE_DEALER_URL"]))
    print(get_ford_mfg_escape_hero_img(const["ESCAPE_MANUFACTURER_IMAGE_URL"]))
    print(get_ford_dealer_escape_hero_img(const["ESCAPE_DEALER_IMAGE_URL"]))

    driver = WebDriverSingleton.get_driver()
    driver.quit()
