import os
import pandas as pd
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import requests

# Define environment variables
username = 'jayshah36262@gmail.com'
password = 'Jayshah12'

# Define MySQL connection parameters
mysql_user = os.getenv('MYSQL_USER', 'root')
mysql_password = os.getenv('MYSQL_PASSWORD', 'root')
mysql_host = '192.168.3.112'
mysql_database = os.getenv('MYSQL_DATABASE', 'my_db')

# Create SQLAlchemy engine for MySQL
engine = create_engine(f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}')

# Fetch data
session = requests.Session()
login_url = "https://www.screener.in/login/?"
login_page = session.get(login_url)
soup = BeautifulSoup(login_page.content, 'html.parser')

# Find the CSRF token
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
login_payload = {
    'username': username,
    'password': password,
    'csrfmiddlewaretoken': csrf_token
}

headers = {
    'Referer': login_url,
    'User-Agent': 'Mozilla/5.0'
}

# Perform login
response = session.post(login_url, data=login_payload, headers=headers)
print(f"Login response URL: {response.url}")

if response.url == "https://www.screener.in/dash/":
    search_url = "https://www.screener.in/company/RELIANCE/consolidated/"
    search_response = session.get(search_url)
    
    if search_response.status_code == 200:
        soup = BeautifulSoup(search_response.content, 'html.parser')
        table = soup.find('table', {'class': 'data-table responsive-text-nowrap'})
        
        if table:
            headers = [th.text.strip() for th in table.find_all('th')]
            rows = table.find_all('tr')
            row_data = [[col.text.strip() for col in row.find_all('td')] for row in rows[1:]]
            
            # Create DataFrame
            df = pd.DataFrame(row_data, columns=headers)
            print("DataFrame created:")
            print(df.head())  # Print the first few rows for inspection

            # Save to CSV
            df.to_csv('profit_and_loss.csv', index=False)
            print("CSV created successfully.")

            # Print DataFrame schema for debugging
            print("DataFrame schema:")
            print(df.dtypes)
            print("Column names:")
            print(df.columns)

            # Handle empty or invalid column names
            if df.columns[0] == '':
                df = df.iloc[:, 1:]
                headers = headers[1:]
            
            df.columns = [col.strip().replace(' ', '_').replace('-', '_') or f'col_{i}' for i, col in enumerate(headers)]
            
            print("Sanitized column names:")
            print(df.columns)

            # Load CSV into MySQL
            try:
                df.to_sql('test', con=engine, if_exists='replace', index=False)
                print("Data successfully loaded into MySQL.")
            except Exception as e:
                print(f"Error loading data into MySQL: {e}")
        else:
            print("Failed to find the data table.")
    else:
        print(f"Failed to retrieve Reliance data. Status Code: {search_response.status_code}")
else:
    print("Login failed.")
