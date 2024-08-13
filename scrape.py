import argparse
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_and_download_file(url, username, password, file_suffix):
    # Hardcoded path to ChromeDriver based on pipeline configuration
    chrome_driver_path = "/usr/local/bin/chromedriver"

    # Use the provided ChromeDriver path
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(url)

    try:
        # Log in
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(concat(" ", @class, " "), " account ")]'))
        ).click()

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_username")]'))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[(@id = "id_password")]'))
        )

        email_input.send_keys(username)
        password_input.send_keys(password)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(concat(" ", @class, " "), " icon-user ")]'))
        ).click()

        # Navigate to the desired page
        driver.get("https://www.screener.in/company/RELIANCE/consolidated/")
        
        # Wait for the download button to be clickable and click it
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[3]/div[1]/form/button'))
        )
        download_button.click()

        # Wait for the download to complete
        time.sleep(30)  # Adjust based on expected download time

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login and download file using Selenium.')
    parser.add_argument('--username', required=True, help='Username for login')
    parser.add_argument('--password', required=True, help='Password for login')
    parser.add_argument('--file_suffix', required=True, help='Suffix for the downloaded file')

    args = parser.parse_args()

    # Call the login and download function with the provided arguments
    login_and_download_file("https://www.screener.in/", args.username, args.password, args.file_suffix)
