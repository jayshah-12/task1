import os
import pandas as pd
from sqlalchemy import create_engine, Integer
from sqlalchemy.types import Integer as SQLInteger
from bs4 import BeautifulSoup
import requests
import time


username = os.getenv('SCRAPER_USERNAME', 'jayshah36262@gmail.com')
password = os.getenv('SCRAPER_PASSWORD', 'Jayshah12')


mysql_user = os.getenv('MYSQL_USER', 'root')
mysql_password = os.getenv('MYSQL_PASSWORD', 'root')
mysql_host = os.getenv('MYSQL_HOST', 'localhost:3307')
mysql_database = os.getenv('MYSQL_DATABASE', 'my_db')

# Create SQLAlchemy engine for MySQL
engine = create_engine(f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}')


companies_df = pd.read_csv('company.csv')  
# print(companies_df.columns)

# Initialize a session
session = requests.Session()
login_url = "https://www.screener.in/login/?"
login_page = session.get(login_url)
soup = BeautifulSoup(login_page.content, 'html.parser')

# Extract CSRF token
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

# Initialize empty DataFrames
combined_data = pd.DataFrame()
combined_ttm = pd.DataFrame()
combined_company = pd.DataFrame(columns=['Company_Name', 'Company_Id'])

if response.url == "https://www.screener.in/dash/":
    for index, row in companies_df.iterrows():
        company_name = row['Company_Name']
        symbol = row['Symbol']
        search_url = f"https://www.screener.in/company/{symbol}/consolidated/"
        search_response = session.get(search_url)
        comp_id = index + 1
        
        if search_response.status_code == 200:
            print(f"Data retrieved successfully for symbol: {symbol}")
            soup = BeautifulSoup(search_response.content, 'html.parser')
            table1 = soup.find('section', {'id': 'profit-loss'})
            table = table1.find('table')
            
            if table:
                headers = [th.text.strip() or f'Column_{i}' for i, th in enumerate(table.find_all('th'))]
                rows = table.find_all('tr')
                row_data = []
                
                for row in rows[1:]:
                    cols = row.find_all('td')
                    cols = [col.text.strip() for col in cols]
                    if len(cols) == len(headers):
                        row_data.append(cols)
                    else:
                        print(f"Row data length mismatch for symbol {symbol}: {cols}")
                
                # Create a DataFrame with sanitized headers
                df = pd.DataFrame(row_data, columns=headers)
                
                # Rename the first column to 'Narration'
                if not df.empty:
                    df.columns = ['Narration'] + df.columns[1:].tolist()
                    df = df.reset_index(drop=True)

                    try:
                        # Attempt to drop 'TTM' column and process DataFrame
                        temp = df.drop(columns=['TTM'])  # DataFrame without TTM
                        data = pd.melt(temp, id_vars=['Narration'], var_name='Year', value_name='Value')  # Melting data without TTM
                        data = data.sort_values(by=['Narration', 'Year']).reset_index(drop=True)
                        data['Value'] = data['Value'].str.replace(',', '').str.replace('%', '').astype(float)
                        # data['ttm_id'] = None
                        data['Company_Id'] = comp_id
                        data['value_type'] = data['Narration'].apply(lambda x: 'percent' if '%' in x else 'crore')
                        # Process the 'ttm' DataFrame
                        ttm = df[['Narration', 'TTM']].copy() 
                        ttm['TTM'] = ttm['TTM'].str.replace(',', '').str.replace('%', '') 
                        # ttm.insert(0, 'id2', range(1, len(ttm) + 1))
                        ttm['Company_Id'] = comp_id
                        # narration_to_id = ttm.set_index('Narration')['id2'].to_dict()
                        # data['ttm_id'] = data['Narration'].map(narration_to_id)
                        ttm['TTM_type'] = ttm['Narration'].apply(lambda x: 'percent' if '%' in x else 'crore')
                        # ttm = ttm.drop(columns=['id2'])
                        combined_data = pd.concat([combined_data, data], ignore_index=True)
                        combined_ttm = pd.concat([combined_ttm, ttm], ignore_index=True)
                        combined_company = pd.concat([combined_company, pd.DataFrame({'Company_Name': [company_name], 'Company_Id': [comp_id]})], ignore_index=True)
                        print(combined_company)
                    # except KeyError as e:
                    #     print(f"Column 'TTM' not found in DataFrame for symbol {symbol}: {e}")
                    #     continue
                    
                    except Exception as e:
                        print(f"Error processing data for symbol {symbol}: {e}")
                        continue 
            else:
                print(f"Failed to find the data table for symbol: {symbol}.")
        else:
            print(f"Failed to retrieve data for symbol: {symbol}. Status Code: {search_response.status_code}")

        time.sleep(3)

    # Save combined DataFrames to SQL
    order_ttm = ['Company_Id', 'Narration', 'TTM','TTM_type']
    combined_ttm = combined_ttm[order_ttm]

    order_data = [ 'Company_Id','Narration', 'Year','Value','value_type']
    combined_data = combined_data[order_data]

    order_company = ['Company_Id','Company_Name']
    combined_company = combined_company[order_company]


    combined_data.to_sql('data', con=engine, if_exists='append', index=True, index_label='id', dtype={'id': SQLInteger()})
    combined_ttm.to_sql('ttm', con=engine, if_exists='append', index=True, index_label='id')
    combined_company.to_sql('companies', con=engine, if_exists='append', index=True)
    print("All data successfully loaded into MySQL.")

else:
    print("Login failed.")
