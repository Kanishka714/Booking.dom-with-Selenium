import os
import time  # Import time module for sleep functionality
from locale import currency
from telnetlib import EC

import driver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from . import constants as const
from selenium.webdriver.common.by import By

class Booking(webdriver.Chrome):
    def __init__(self, driver_path='/opt/homebrew/bin/chromedriver', teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        # Correct the PATH adjustment
        os.environ['PATH'] += os.pathsep + self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
        time.sleep(20)  # Wait for 20 seconds after loading the first page

    def cancel_registration(self):
        wait = WebDriverWait(self, 10)
        try:
            # Wait for the pop-up close button to be clickable and click it
            close_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[data-testid="selection-item"]')
                )
            )
            close_button.click()

            print("Pop-up closed successfully.")
        except Exception as e:
            print(f"An error occurred while trying to close the pop-up: {e}")

    def change_currency(self, currency_code):
        # Use WebDriverWait to wait for the currency button to be clickable
        wait = WebDriverWait(self, 10)
        try:
            # Wait for the currency button and click it
            currency_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]'))
            )
            currency_button.click()

            # Get all 14 ul tags
            ul_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul')))

            # Loop through each ul and its respective li tags
            for ul in ul_elements:
                li_elements = ul.find_elements(By.TAG_NAME, 'li')
                for li in li_elements:
                    # Get the text inside each li element
                    li_text = li.text.strip()

                    # Check if the text contains the currency code
                    if currency_code in li_text:
                        # Find the button inside this li and click it
                        currency_button = li.find_element(By.CSS_SELECTOR, 'button[data-testid="selection-item"]')
                        currency_button.click()

                        print(f"Currency {currency_code} selected successfully.")
                        return

            print(f"Currency {currency_code} not found.")

        except Exception as e:
            print(f"An error occurred while trying to select the currency: {e}")