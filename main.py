from locale import currency

import booking

from booking.booking import Booking

with Booking(teardown=False) as bot:
    bot.land_first_page()
    currency_code = 'ARS'  # Manually set your desired currency code here
    bot.change_currency(currency_code)
    bot.select_place_to_go('Galle')
    bot.select_dates(check_in='2024-09-16' , check_out='2024-09-17')
    bot.select_occupiers(adult_count=5, child_count=2, room_count=2)
    input("Press Enter to close the browser...")  # Keeps the browser open
    print('Exiting...')
