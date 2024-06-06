import unittest
from unittest.mock import patch
import asyncio
from bs4 import BeautifulSoup
from bot import createpost, close_bot, send_error_to_admin
from config import LEVEL

class TestPoolProcessing(unittest.TestCase):

    @patch('main.initialize_db')
    @patch('main.insert_pool')
    @patch('main.select_pool_by_title')
    @patch('main.webdriver.Chrome')
    @patch('main.BeautifulSoup')
    def test_fetch_and_process_pools(self, mock_bs, mock_chrome, mock_select, mock_insert, mock_db):
        # Mock database initialization
        mock_conn = mock_db.return_value

        # Mock select_pool_by_title to return False (pool not in database)
        mock_select.return_value = False

        # Mock BeautifulSoup to return a fake pool
        fake_html = '<li class="_item_kyzjh_6"><div class="_title_1xl6z_82">Test Pool</div><span class="_perHour_1atj8_36">1000 $/hour</span><div class="_imageContainer_1atj8_22"><img src="image_source"></div></li>'
        mock_soup = mock_bs.return_value
        mock_soup.find_all.return_value = BeautifulSoup(fake_html, 'html.parser').find_all('li')

        # Determine per_hour value based on LEVEL
        level_values = {
            "Bronze": 0.016,
            "Silver": 0.16,
            "Gold": 16,
            "Platinum": 80
        }
        per_hour_value = level_values.get(LEVEL)  # Default to Silver if LEVEL is not found
        per_hour = f"{per_hour_value} $/hour"

        # Mock data to be used in the test
        title = "Test Pool"
        img_src = "image_source"

        try:
            # Run the createpost function directly with asyncio
            asyncio.run(createpost(title, per_hour, img_src))

            # Ensure the bot session is closed after the test
            asyncio.run(close_bot())

            # Send a message to the admin indicating no errors
            asyncio.run(send_error_to_admin("Test. No errors"))

        except Exception as e:
            asyncio.run(send_error_to_admin({str(e)}))
            raise

if __name__ == '__main__':
    unittest.main()
