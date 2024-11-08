import pandas as pd
from datetime import datetime
import pytz
import os

# Function to convert timestamp from UTC to Brisbane time
def convert_to_brisbane_time(timestamp_str):
    # Define the format of the timestamp in the Excel file
    timestamp_format = "%d/%m/%Y %I:%M:%S %p"  # Adjust if the format is different
    
    # Parse the timestamp to a datetime object in UTC
    utc_time = datetime.strptime(timestamp_str, timestamp_format)
    
    # Define timezones
    utc_zone = pytz.utc
    brisbane_zone = pytz.timezone('Australia/Brisbane')
    
    # Localize to UTC and convert to Brisbane time
    utc_dt = utc_zone.localize(utc_time)
    brisbane_dt = utc_dt.astimezone(brisbane_zone)
    
    # Return as a formatted string
    return brisbane_dt.strftime("%Y-%m-%d %H:%M:%S")

# Prompt for file input using WSL
input_file = input("Please enter the path to the Excel file: ")
output_file = "converted_brisbane_time.xlsx"

# Check if the input file exists
if not os.path.exists(input_file):
    print("File not found. Please check the path and try again.")
else:
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Check if 'ZTIMESTAMP' column exists
    if 'ZTIMESTAMP' not in df.columns:
        print("'ZTIMESTAMP' column not found in the Excel file.")
    else:
        # Convert 'ZTIMESTAMP' from UTC to Brisbane time
        df['ZTIMESTAMP_Brisbane'] = df['ZTIMESTAMP'].apply(convert_to_brisbane_time)
        
        # Save the new DataFrame to an Excel file
        df.to_excel(output_file, index=False)
        print(f"Converted timestamps saved to {output_file}")



# input run script on raw excel data location table. 