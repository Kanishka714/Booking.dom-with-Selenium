import os
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

    def change_currency(self):
        # Use WebDriverWait to wait for the button to be clickable
        wait = WebDriverWait(self, 10)
        try:
            # Wait until the button is clickable
            currency_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')))
            currency_button.click()
        except Exception as e:
            print(f"An error occurred while trying to click the currency button: {e}")