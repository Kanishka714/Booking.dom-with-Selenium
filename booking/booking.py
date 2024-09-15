import os
import time
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
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(BASE_URL)  # Load the base URL
        time.sleep(20)  # Wait for the page to fully load

    def cancel_registration(self):
        """Checks and closes the registration pop-up if it appears."""
        wait = WebDriverWait(self, 5)
        try:
            close_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="selection-item"]'))
            )
            close_button.click()
            print("Pop-up closed successfully.")
        except Exception:
            pass  # If pop-up is not present, continue

    def ensure_no_popup(self):
        """Ensure any pop-up is closed before proceeding."""
        self.cancel_registration()

    def change_currency(self, currency_code):
        """Changes the currency based on the provided currency code."""
        self.ensure_no_popup()
        wait = WebDriverWait(self, 10)
        try:
            # Click the currency picker button
            currency_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]'))
            )
            currency_button.click()

            # Get all ul tags
            ul_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul')))

            for ul in ul_elements:
                li_elements = ul.find_elements(By.TAG_NAME, 'li')
                for li in li_elements:
                    li_text = li.text.strip()

                    if currency_code in li_text:
                        currency_button = li.find_element(By.CSS_SELECTOR, 'button[data-testid="selection-item"]')
                        currency_button.click()
                        print(f"Currency {currency_code} selected successfully.")
                        return

            print(f"Currency {currency_code} not found.")
        except Exception as e:
            print(f"An error occurred while trying to select the currency: {e}")
            self.ensure_no_popup()

    def select_place_to_go(self, place_to_go):
        """Enters the destination to search for."""
        try:
            self.ensure_no_popup()  # Check for pop-up
            search_field = self.find_element(By.NAME, value='ss')
            search_field.clear()
            search_field.send_keys(place_to_go)

            # Wait for 5 seconds before selecting the first result
            time.sleep(5)

            first_result = self.find_element(By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]')
            first_result.click()

            self.ensure_no_popup()  # Check for pop-up again
        except Exception as e:
            print(f"An error occurred while selecting the destination: {e}")
            self.ensure_no_popup()  # Ensure the pop-up is closed if it blocks the input

    def select_dates(self, check_in, check_out):
        self.ensure_no_popup()  # Check for pop-up
        try:
            check_in_element = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_in}"]')
            check_in_element.click()

            check_out_element = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_out}"]')
            check_out_element.click()
        except Exception as e:
            print(f"An error occurred while selecting dates: {e}")
            self.ensure_no_popup()  # Ensure the pop-up is closed if it blocks the input

    def select_occupiers(self, adult_count, child_count, room_count):
        """Selects the number of adults, children, and rooms."""
        try:
            self.ensure_no_popup()  # Check for pop-up

            # Handle the adult count
            if adult_count == 1:
                # Wait for the first button (decrease button) in the adults section
                first_button = WebDriverWait(self, 20).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '.aaf77d2184 > .a7a72174b8:first-of-type button:first-of-type'))
                )
                first_button.click()
                print("Adult count set to 1 by clicking the decrease button.")

            elif adult_count > 2:
                # Click the "increase" button the necessary number of times
                for _ in range(adult_count - 2):
                    increase_button = WebDriverWait(self, 20).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, '.aaf77d2184 > .a7a72174b8:nth-of-type(1) button:nth-of-type(2)'))
                    )
                    increase_button.click()
                    print(f"Increase button clicked. Current adult count: {_ + 2}")

            # Handle the child count
            if child_count > 0:
                for _ in range(child_count):
                    # Adjusted selector for the child increase button
                    child_increase_button = WebDriverWait(self, 20).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, '.bfb38641b0 button:nth-of-type(2)')
                        )
                    )
                    child_increase_button.click()
                    print(f"Increase button clicked for child {_ + 1}")

            # Handle the room count
            if room_count > 1:
                for _ in range(room_count - 1):
                    # Adjusted selector for the room increase button
                    room_increase_button = WebDriverWait(self, 20).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, '.bfb38641b0 button:nth-of-type(2)')
                        )
                    )
                    room_increase_button.click()
                    print(f"Increase button clicked for room {_ + 2}")

        except Exception as e:
            print(f"An error occurred while selecting occupiers: {e}")
            self.ensure_no_popup()  # Ensure the pop-up is closed if it blocks the input