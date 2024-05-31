import asyncio
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from config import URL_SILVER, CHROME_DRIVER_PATH, DB_FILE
from db import initialize_db, insert_pool, select_pool_by_title
from bot import createpost

async def fetch_and_process_pools():
    # Настройка Selenium
    options = Options()
    options.add_argument("--headless")  # Запуск в фоновом режиме
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Добавлено
    options.add_argument("--remote-debugging-port=9222")  # Добавлено
    service = Service(CHROME_DRIVER_PATH)

    # Инициализация базы данных
    conn = initialize_db(DB_FILE)

    while True:
        try:
            # Инициализация браузера
            driver = webdriver.Chrome(service=service, options=options)

            # Открытие страницы авторизации
            driver.get(URL_SILVER)

            # Ожидание загрузки страницы
            time.sleep(5)

            # Получение HTML-кода страницы
            html = driver.page_source

            # Парсинг HTML с помощью BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Поиск всех элементов пулов
            pools = soup.find_all('li', class_='_item_kyzjh_6')

            print(f"Найдено пулов: {len(pools)}")

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
                        print(f"Pool '{title}' already exists in the database.")
                else:
                    print("Один из элементов не найден:")
                    print(f"Title Element: {title_element}")
                    print(f"Per Hour Element: {per_hour_element}")
                    print(f"Image Element: {img_element}")

            # Закрытие браузера
            driver.quit()

        except Exception as e:
            print(f"Ошибка: {e}")

        # Повторить через минуту
        await asyncio.sleep(55)

    # Закрытие соединения с базой данных
    conn.close()

async def main():
    await fetch_and_process_pools()

if __name__ == "__main__":
    asyncio.run(main())