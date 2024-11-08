# SANTO WAL FILE

import pandas as pd
import simplekml
from datetime import datetime

# Define the file paths
input_file = "/mnt/c/Users/c2buc/Downloads/Santo WAL Location log P2000412130.csv"
output_file = "/mnt/c/Users/c2buc/Downloads/Santo WAL Location log P2000412130.kml"

# Print statements to confirm the paths being used
print(f"Opening CSV file: {input_file}")
print(f"Saving KML file to: {output_file}")

# Load the TSV file into a DataFrame
df = pd.read_csv(input_file, sep='\t', encoding='utf-16')  # Use tab separator and adjust encoding as needed

# Drop the 'time' column if it exists
if 'time' in df.columns:
    df = df.drop(columns=['time'])

# Print the first few rows to confirm data is loaded correctly
print("Data loaded from TSV without 'time' column:")
print(df.head())

# Define the date and time range for filtering
start_datetime = datetime.strptime("2020/09/13 14:00:00", "%Y/%m/%d %H:%M:%S")
end_datetime = datetime.strptime("2020/09/13 22:00:00", "%Y/%m/%d %H:%M:%S")

# Create a new KML object
kml = simplekml.Kml()

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Parse the timestamp to a datetime object
    timestamp_str = row['time_string']
    timestamp_dt = datetime.strptime(timestamp_str, "%Y/%m/%d %H:%M:%S")

    # Check if the timestamp is within the specified range
    if start_datetime <= timestamp_dt <= end_datetime:
        # Format the timestamp to ISO 8601 format for KML (e.g., "2020-09-13T14:30:00Z")
        iso_timestamp = timestamp_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Create a point for each row that falls within the time range
        pnt = kml.newpoint()
        
        # Set the name as the time_string
        display_time = row['time_string']
        pnt.name = display_time
        print(f"\nCreating point {index + 1}:")
        print(f"Display Time (Name): {pnt.name}")
        
        # Set the coordinates (longitude, latitude)
        pnt.coords = [(row['longitude'], row['latitude'])]
        print(f"Coordinates: Longitude = {row['longitude']}, Latitude = {row['latitude']}")
        
        # Add a TimeStamp element for each point to enable the time slider in Google Earth
        pnt.timestamp.when = iso_timestamp

        # Construct the description field, using only the specified columns
        description = (
            f"Time: {display_time}\n"
            f"Latitude: {row['latitude']}\n"
            f"Longitude: {row['longitude']}\n"
            f"Altitude: {row['altitude']} m\n"
            f"Provider: {row['provider']}\n"
            f"Accuracy: {row['accuracy']} m\n"
            f"Bearing: {row['bearing']}°\n"
            f"Speed: {row['speed']} m/s\n"
            f"Timezone: {row['timezone_id'] if 'timezone_id' in row else 'N/A'}"
        )
        pnt.description = description
        print("Description:")
        print(description)

# Save the KML file to the specified path
kml.save(output_file)
print(f"\nKML file '{output_file}' created successfully.")


