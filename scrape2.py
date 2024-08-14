import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Retrieve credentials from environment variables
username = "jayshah36262@gmail.com"
password = "Jayshah12"

if not username or not password:
    raise ValueError("Username or Password environment variables are not set.")

# Start a session
session = requests.Session()

# Get the login page to retrieve the CSRF token
login_url = "https://www.screener.in/login/?"
login_page = session.get(login_url)
soup = BeautifulSoup(login_page.content, 'html.parser')

# Find the CSRF token in the login form (usually in a hidden input field)
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

# Prepare the login payload
login_payload = {
    'username': username,
    'password': password,
    'csrfmiddlewaretoken': csrf_token
}

# Include the Referer header as required
headers = {
    'Referer': login_url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

# Send the login request
response = session.post(login_url, data=login_payload, headers=headers)
print(response.url)

# Check if login was successful
if response.url == "https://www.screener.in/dash/":
    print("Login successful")
    
    # Now navigate to the Reliance company page
    search_url = "https://www.screener.in/company/RELIANCE/consolidated/"
    search_response = session.get(search_url)
    if search_response.status_code == 200:
        print("Reliance data retrieved successfully")
        soup = BeautifulSoup(search_response.content, 'html.parser')

        table = soup.find('table', {'class': 'data-table responsive-text-nowrap'})
        headers = [th.text.strip() for th in table.find_all('th')]

        rows = table.find_all('tr')
        row_data = []

        for row in rows[1:]:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            row_data.append(cols)

        df = pd.DataFrame(row_data, columns=headers)
        print(df)
        df.to_csv('profit_and_loss.csv', index=False)
    else:
        print("Failed to retrieve Reliance data. Status Code:", search_response.status_code)
else:
    print("Login failed. Response URL:", response.url)
