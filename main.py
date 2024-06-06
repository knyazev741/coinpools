import asyncio
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from config import URL, CHROME_DRIVER_PATH, DB_FILE
from db import initialize_db, insert_pool, select_pool_by_title
from bot import createpost, close_bot, send_error_to_admin

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def fetch_and_process_pools():
    # Configure Selenium
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Added
    options.add_argument("--remote-debugging-port=9222")  # Added
    service = Service(CHROME_DRIVER_PATH)

    # Initialize the database
    conn = initialize_db(DB_FILE)

    while True:
        try:
            # Initialize the browser
            driver = webdriver.Chrome(service=service, options=options)

            # Open the login page
            driver.get(URL)

            # Wait for the page to load
            await asyncio.sleep(5)

            # Get the HTML source of the page
            html = driver.page_source

            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Find all pool elements
            pools = soup.find_all('li', class_='_item_kyzjh_6')

            logger.info(f"Found pools: {len(pools)}")

            for pool in pools:
                title_element = pool.find('div', class_='_title_1xl6z_82')
                per_hour_element = pool.find('span', class_='_perHour_1atj8_36')
                img_element = pool.find('div', class_='_imageContainer_1atj8_22').find('img')

                if title_element and per_hour_element and img_element:
                    title = title_element.text.strip()
                    per_hour = per_hour_element.text.strip()
                    img_src = img_element['src']

                    if not select_pool_by_title(conn, title):
                        pool_data = (title, per_hour, img_src)
                        insert_pool(conn, pool_data)
                        await createpost(title, per_hour, img_src)
                    else:
                        logger.info(f"Pool '{title}' already exists in the database.")
                else:
                    logger.warning("One of the elements was not found:")
                    logger.warning(f"Title Element: {title_element}")
                    logger.warning(f"Per Hour Element: {per_hour_element}")
                    logger.warning(f"Image Element: {img_element}")

            # Close the browser
            driver.quit()

        except Exception as e:
            logger.error(f"Error: {e}")
            await send_error_to_admin(str(e))

        # Repeat after a minute
        await asyncio.sleep(55)

    # Close the database connection
    conn.close()


async def main():
    try:
        await fetch_and_process_pools()
    finally:
        await close_bot()

if __name__ == "__main__":
    asyncio.run(main())
