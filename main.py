import pandas as pd
import simplekml
from datetime import datetime

# Define the file paths
input_file = "/mnt/c/Users/c2buc/Downloads/P2000412133-13.9.2020-Location & Travel-Cached Locations.csv"
output_file = "/mnt/c/Users/c2buc/Downloads/P2000412133-13.9.2020-Location & Travel-Cached Locations.kml"

# Print statements to confirm the paths being used
print(f"Opening CSV file: {input_file}")
print(f"Saving KML file to: {output_file}")

# Load the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Print the first few rows to confirm data is loaded correctly
print("Data loaded from CSV:")
print(df.head())

# Create a new KML object
kml = simplekml.Kml()

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Parse the timestamp to a datetime object
    timestamp_str = row['Timestamp Date/Time - UTC+10:00 (d/MM/yyyy)']
    timestamp_dt = datetime.strptime(timestamp_str, "%d/%m/%Y %I:%M:%S.%f %p")

    # Format the timestamp to ISO 8601 format for KML (e.g., "2020-09-13T14:30:00Z")
    iso_timestamp = timestamp_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Create a point for each row
    pnt = kml.newpoint()
    
    # Set the name as the 12-hour time (to the minute) with AM/PM, removing leading zero from the hour
    name_time = timestamp_dt.strftime("%I:%M %p").lstrip("0")  # Remove leading zero
    pnt.name = name_time
    print(f"\nCreating point {index + 1}:")
    print(f"Time (Name): {pnt.name}")
    
    # Set the coordinates (longitude, latitude)
    pnt.coords = [(row['Longitude'], row['Latitude'])]
    print(f"Coordinates: Longitude = {row['Longitude']}, Latitude = {row['Latitude']}")
    
    # Add a TimeStamp element for each point to enable the time slider in Google Earth
    pnt.timestamp.when = iso_timestamp

    # Construct the description field, including the full time with seconds and date in 12-hour format
    full_time = timestamp_dt.strftime("%I:%M:%S %p").lstrip("0")  # Remove leading zero in full time
    full_date = timestamp_dt.strftime("%d/%m/%Y")  # Format the date as DD/MM/YYYY
    description = (
        f"Date: {full_date}\n"
        f"Full Time: {full_time}\n"
        f"Accuracy: {row['Accuracy (m)']} m\n"
        f"Altitude: {row['Altitude (m)']} m\n"
        f"Altitude Accuracy: {row['Altitude Accuracy (m)']} m\n"
        f"Direction: {row['Direction']}°\n"
        f"Speed: {row['Speed (m/s)']} m/s\n"
        f"Source: {row['Source']}\n"
        f"Location: {row['Location']}"
    )
    pnt.description = description
    print("Description:")
    print(description)

# Save the KML file to the specified path
kml.save(output_file)
print(f"\nKML file '{output_file}' created successfully.")
