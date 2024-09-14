import booking

from booking.booking import Booking

with Booking(teardown=False) as bot:
    bot.land_first_page()
    bot.change_currency()
    input("Press Enter to close the browser...")  # Keeps the browser open
    print('Exiting...')