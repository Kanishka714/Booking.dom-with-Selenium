from locale import currency

import booking

from booking.booking import Booking

with Booking(teardown=False) as bot:
    bot.land_first_page()
    currency_code = 'BRL'  # Manually set your desired currency code here
    bot.change_currency(currency_code)
    input("Press Enter to close the browser...")  # Keeps the browser open
    print('Exiting...')