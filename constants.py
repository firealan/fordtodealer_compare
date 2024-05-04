constants = {
    # Web driver configuration settings
    "web_driver_configuration": {
        "browser_driver_type": "firefox",
        "headless_mode": True,
        "time_sleep": 3,
    },
    # Email configuration settings
    "email_configuration": {
        "skip_flag": False,
        "image_skip_flag": True,
    },
    # Navigation configuration settings
    "navigation_configuration": {
        "skip_flag": False,
        "model_list": ["BRONCO SPORT", "EDGE", "ESCAPE", "F-150", "MUSTANG"],
        "category_list": ["Electrified"],
        # Manufacturer configuration settings
        "manufacturer_configuration": {
            "url": "https://www.ford.ca",
            "main_menu_button_xpath": "//li[@class='main-nav-item no-float-md flyout-item-wrap']/button",
            "sub_menu_button_xpath": "//button[contains(@class,'bri-nav__list-link segment-anchor-trigger fgx-btn')]//span[@class='link-text']",
            "trim_name_xpath": "//div[@class='vehicle-segment-layout fgx-brand-global-container-pad segment-menu-item-container open']//a[@class='veh-item-inline']",
            "trim_price_xpath": "//div[@class='vehicle-segment-layout fgx-brand-global-container-pad segment-menu-item-container open']//span[contains(@data-pricing-template,'price')]",
        },
        # Dealer configuration settings
        "dealer_configuration": {
            "url": "https://fordtodealers.ca",
            "main_menu_button_xpath": "//li[@class='main-nav-item no-float-md flyout-item-wrap']/button",
            "sub_menu_button_xpath": "//button[contains(@class,'bri-nav__list-link segment-anchor-trigger fgx-btn')]//span[@class='link-text']",
            "trim_name_xpath": "//div[@class='vehicle-segment-layout fgx-brand-global-container-pad segment-menu-item-container open']//a[@class='veh-item-inline']",
            "trim_price_xpath": "//div[@class='vehicle-segment-layout fgx-brand-global-container-pad segment-menu-item-container open']//span[contains(@data-pricing-template,'price')]",
        },
    },
    # Vehicle configuration settings
    "vehicle_configuration": {
        "vehicles": [
            # Bronco configuration
            {
                "model": "BRONCO®",
                "skip_flag": True,
                "manufacturer_configuration": {
                    "url": "https://www.ford.ca/suvs/bronco/models/?gnav=vhpnav-specs",
                    "hero_image_url": "https://www.ford.ca/suvs/bronco/?gnav=header-suvs-vhp",
                    "buttons_xpath": None,
                    "trim_name_xpath": "//a[@class='to-checkbox fgx-lnc-btm-brdr-hover']",
                    "trim_price_xpath": '//span[@class="make-info price bri-txt body-three ff-b"]//span[contains(@data-pricing-template, "{price}")]',
                },
                "dealer_configuration": {
                    "url": "https://fordtodealers.ca/ford-bronco/",
                    "hero_image_url": "https://fordtodealers.ca/ford-bronco/",
                    "buttons_xpath": "(//div[@class='owl-dots'])[1]/button",
                    "trim_name_xpath": "//*[contains(@class,'modelChecker')]",
                    "trim_price_xpath": "//*[contains(@class,'priceChecker')]",
                },
            },
            # Bronco Sport configuration
            {
                "model": "BRONCO® SPORT",
                "skip_flag": True,
                "manufacturer_configuration": {
                    "url": "https://www.ford.ca/suvs/bronco-sport/models/?gnav=vhpnav-specs",
                    "hero_image_url": "https://www.ford.ca/suvs/bronco-sport/?gnav=vhpnav-overiew",
                    "buttons_xpath": None,
                    "trim_name_xpath": "//a[@class='to-checkbox fgx-lnc-btm-brdr-hover']",
                    "trim_price_xpath": '//span[@class="make-info price bri-txt body-three ff-b"]//span[contains(@data-pricing-template, "{price}")]',
                },
                "dealer_configuration": {
                    "url": "https://fordtodealers.ca/ford-bronco/",
                    "hero_image_url": "https://fordtodealers.ca/ford-bronco/",
                    "buttons_xpath": "(//div[@class='owl-dots'])[1]/button",
                    "trim_name_xpath": "https://fordtodealers.ca/ford-bronco-sport/",
                    "trim_price_xpath": "https://fordtodealers.ca/ford-bronco-sport/",
                },
            },
            # Edge configuration
            {
                "model": "EDGE®",
                "skip_flag": False,
                "manufacturer_configuration": {
                    "url": "https://www.ford.ca/suvs-crossovers/edge/?gnav=header-suvs-vhp",
                    "hero_image_url": "https://www.ford.ca/suvs-crossovers/edge/?gnav=header-suvs-vhp",
                    "buttons_xpath": "(//ol[@class='bds-carousel-indicators global-indicators to-fade-in  scrollable'])/li",
                    "trim_name_xpath": "//*[@class='fgx-brand-ds to-fade-in title-three ff-d']",
                    "trim_price_xpath": '//*[@class="price"]',
                },
                "dealer_configuration": {
                    "url": "https://fordtodealers.ca/ford-edge/",
                    "hero_image_url": "https://fordtodealers.ca/ford-edge/",
                    "buttons_xpath": "(//div[@class='owl-dots'])[1]/button",
                    "trim_name_xpath": "//*[contains(@class,'modelChecker')]",
                    "trim_price_xpath": "//*[contains(@class,'priceChecker')]",
                },
            },
            # Escape configuration
            {
                "model": "ESCAPE",
                "skip_flag": False,
                "manufacturer_configuration": {
                    "url": "https://www.ford.ca/suvs-crossovers/escape/?gnav=header-suvs-vhp",
                    "hero_image_url": "https://www.ford.ca/suvs-crossovers/escape/?gnav=header-suvs-vhp",
                    "buttons_xpath": None,
                    "trim_name_xpath": "//*[@class='bri-txt generic-title-one ff-b']",
                    "trim_price_xpath": '//*[@class="bri-txt body-one ff-b"]',
                },
                "dealer_configuration": {
                    "url": "https://fordtodealers.ca/ford-escape/",
                    "hero_image_url": "https://fordtodealers.ca/ford-escape/",
                    "buttons_xpath": None,
                    "trim_name_xpath": "//div[contains(@class,'modelChecker')]/div/ul/li/a/span",
                    "trim_price_xpath": "//div[contains(@class,'modelChecker')]/div/ul/li/a/span/label",
                },
            },
            # F-150 configuration
            {
                "model": "F-150®",
                "skip_flag": False,
                "manufacturer_configuration": {
                    "url": "https://www.ford.ca/trucks/f150/?gnav=header-trucks-vhp",
                    "hero_image_url": "https://www.ford.ca/trucks/f150/?gnav=header-trucks-vhp",
                    "buttons_xpath": None,
                    "trim_name_xpath": "//*[@class='bri-txt generic-title-one ff-b']",
                    "trim_price_xpath": '//div[@class="model-walk-tab-price-disclosure-container"]//span[contains(@data-pricing-template, "{price}")]',
                },
                "dealer_configuration": {
                    "url": "https://fordtodealers.ca/ford-f-150/",
                    "hero_image_url": "https://fordtodealers.ca/ford-f-150/",
                    "buttons_xpath": "(//div[@class='owl-dots'])[1]/button",
                    "trim_name_xpath": "//*[contains(@class,'modelChecker')]",
                    "trim_price_xpath": "//*[contains(@class,'priceChecker')]",
                },
            },
            # Mustang configuration
            {
                "model": "MUSTANG®",
                "skip_flag": False,
                "manufacturer_configuration": {
                    "url": "https://www.ford.ca/cars/mustang/?gnav=header-suvs-vhp",
                    "hero_image_url": "https://www.ford.ca/cars/mustang/?gnav=header-suvs-vhp",
                    "buttons_xpath": "(//ol[@class='bds-carousel-indicators global-indicators to-fade-in  scrollable'])/li",
                    "trim_name_xpath": "//*[@class='fgx-brand-ds to-fade-in title-three ff-d']",
                    "trim_price_xpath": '//*[@class="price"]',
                },
                "dealer_configuration": {
                    "url": "https://fordtodealers.ca/ford-mustang/",
                    "hero_image_url": "https://fordtodealers.ca/ford-mustang/",
                    "buttons_xpath": "(//div[@class='owl-dots'])[1]/button",
                    "trim_name_xpath": "//*[contains(@class,'modelChecker')]",
                    "trim_price_xpath": "//*[contains(@class,'priceChecker')]",
                },
            },
        ]
    },
}
