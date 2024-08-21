import pandas as pd
import os

# Define the file path
file_path = 'profit_and_loss.xlsx'

# Check if the file exists
if os.path.exists(file_path):
    # Load the Excel file into a Pandas DataFrame
    df = pd.read_excel(file_path)
    
    # Print the DataFrame (or process it as needed)
    print(df.head(15))
else:
    print(f'{file_path} not found.')
