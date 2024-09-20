import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from booking.constants import BASE_URL

class Booking(webdriver.Chrome):
    def __init__(self, driver_path='/opt/homebrew/bin/chromedriver', teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += os.pathsep + self.driver_path
        super().__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(BASE_URL)  # Load the base URL
        self.ensure_no_popup()  # Check and close pop-up after landing on the page

    def ensure_no_popup(self):
        """Ensure any pop-up is closed before proceeding."""
        try:
            close_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="selection-item"]'))
            )
            close_button.click()
            print("Pop-up closed successfully.")
        except Exception as e:
            print(f"No pop-up found or unable to close pop-up: {e}")

    def change_currency(self, currency_code):
        """Changes the currency based on the provided currency code."""
        self.ensure_no_popup()
        wait = WebDriverWait(self, 10)
        try:
            currency_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]'))
            )
            currency_button.click()

            ul_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul')))
            for ul in ul_elements:
                li_elements = ul.find_elements(By.TAG_NAME, 'li')
                for li in li_elements:
                    li_text = li.text.strip()
                    if currency_code in li_text:
                        li.find_element(By.CSS_SELECTOR, 'button[data-testid="selection-item"]').click()
                        print(f"Currency {currency_code} selected successfully.")
                        return

            print(f"Currency {currency_code} not found.")
        except Exception as e:
            print(f"An error occurred while trying to select the currency: {e}")
        self.ensure_no_popup()  # Check and close pop-up after changing currency

    def select_place_to_go(self, place_to_go):
        """Enters the destination to search for."""
        self.ensure_no_popup()
        try:
            search_field = self.find_element(By.NAME, value='ss')
            search_field.clear()
            search_field.send_keys(place_to_go)

            # Wait for the first result
            first_result = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]'))
            )
            first_result.click()
        except Exception as e:
            print(f"An error occurred while selecting the destination: {e}")
        self.ensure_no_popup()

    def open_date_picker(self):
        """Click the div element to open the date picker."""
        self.ensure_no_popup()
        try:
            date_picker_trigger = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.a1139161bf'))
            )
            date_picker_trigger.click()
            print("Date picker triggered successfully.")
        except Exception as e:
            print(f"An error occurred while opening the date picker: {e}")

    def select_dates(self, check_in, check_out):
        """Selects check-in and check-out dates."""
        self.ensure_no_popup()
        try:
            self.open_date_picker()
            check_in_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{check_in}"]'))
            )
            check_in_element.click()
            print(f"Check-in date {check_in} selected.")

            check_out_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{check_out}"]'))
            )
            check_out_element.click()
            print(f"Check-out date {check_out} selected.")
        except Exception as e:
            print(f"An error occurred while selecting dates: {e}")
        self.ensure_no_popup()

    def select_occupiers(self, adult_count, child_count, room_count):
        """Selects the number of adults, children, and rooms."""
        self.ensure_no_popup()
        try:
            # Open the occupancy selection div
            open_div = WebDriverWait(self, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.d777d2b248'))
            )
            open_div.click()
            print("Div opened successfully.")

            # Handle adult count
            adult_increase_button = WebDriverWait(self, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '.aaf77d2184 > .a7a72174b8:nth-of-type(1) button:nth-of-type(2)'))
            )
            for _ in range(adult_count - 2):
                adult_increase_button.click()
                print(f"Adult count increased to: {_ + 2}")

            # Handle child count
            child_increase_button = WebDriverWait(self, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.a7a72174b8:nth-of-type(2) button:nth-of-type(2)'))
            )
            for _ in range(child_count):
                child_increase_button.click()
                print(f"Child count increased to: {_ + 1}")

            # Click the done button
            done_button = WebDriverWait(self, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.a83ed08757.c21c56c305.bf0537ecb5'))
            )
            done_button.click()
            print("Occupancy selection done.")

        except Exception as e:
            print(f"An error occurred while selecting occupiers: {e}")