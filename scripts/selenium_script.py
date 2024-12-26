from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import os

def fetch_trends():

    start_time = datetime.now()

    hostname = os.getenv('HOSTNAME')
    port = os.getenv('PORT')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    options = {
        'proxy': {
            'http': f'http://{username}:{password}@{hostname}:{port}',
            'https': f'http://{username}:{password}@{hostname}:{port}',
            'no_proxy': 'localhost,127.0.0.1'  # Bypass the proxy for local addresses
        }
    }

    profile_path = "/Users/apple/Library/Application Support/Google/Chrome/Profile 1"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={profile_path}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        seleniumwire_options=options,
        options=chrome_options
    )

    try:
        driver.get('https://httpbin.org/ip')
        time.sleep(1)
        ip_address = driver.find_element(By.TAG_NAME, 'pre').text
        print(f"IP Address: {ip_address}")

        # Log into Twitter
        driver.get("https://x.com/i/flow/login")
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "text"))
        )
        print("On login page...")

        input_username = driver.find_element(By.NAME, "text")
        input_username.send_keys("rishidhingra777")
        input_username.send_keys(Keys.RETURN)

        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "text"))
        )

        input_email = driver.find_element(By.NAME, "text")
        input_email.send_keys("rishidhingra777@gmail.com")
        input_email.send_keys(Keys.RETURN)

        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )

        input_password = driver.find_element(By.NAME, "password")
        input_password.send_keys("Twitter@10")
        input_password.send_keys(Keys.RETURN)

        time.sleep(1)

        # Navigate to trends page
        driver.get("https://twitter.com/explore/tabs/trending")
        time.sleep(1)

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, './/div[@data-testid="cellInnerDiv"]'))
        )

        cards = driver.find_elements(By.XPATH, './/div[@data-testid="cellInnerDiv"]')
        print(f"Number of trending cards found: {len(cards)}")
        # time.sleep(5)

        trends = []
        for i in range(min(5, len(cards))):
            try:
                title_element = cards[i].find_element(By.XPATH, './/div[contains(@class, "css-146c3p1")]/span/span')
                title = title_element.text
                trends.append(title)
            except Exception as e:
                print(f"Error extracting title for card {i+1}: {e}")
                trends.append(f"Card {i+1}: Title not found")

    except TimeoutException as e:
        print(f"Timeout error: {e}. Setting default trends.")
        trends = [
            "Trending Topic 1",
            "Trending Topic 2",
            "Trending Topic 3",
            "Trending Topic 4",
            "Trending Topic 5"
        ]
    finally:
        end_time = datetime.now()
        driver.quit()
        record = {
            "_id": "XXXXXXX",
            "trends": trends
        }
        return {
            "trends": trends,
            "ip_address": ip_address.split(":")[1].strip(),  # Extract the actual IP address from the response
            "record": record,
            "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": end_time.strftime('%Y-%m-%d %H:%M:%S')
        }