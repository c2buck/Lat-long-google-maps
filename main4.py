import pandas as pd
import simplekml
from datetime import datetime

# Define the file paths
input_file = "/mnt/c/Users/c2buc/Downloads/P2000412780-13.9.2020-Location & Travel-Cached Locations.csv"
output_file = "/mnt/c/Users/c2buc/Downloads/SPEED - P2000412780-13.9.2020-Location & Travel-Cached Locations.kml"

# Print statements to confirm the paths being used
print(f"Opening CSV file: {input_file}")
print(f"Saving KML file to: {output_file}")

# Load the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Print the first few rows to confirm data is loaded correctly
print("Data loaded from CSV:")
print(df.head())

# Define the time range for filtering
start_time = datetime.strptime("16:50", "%H:%M").time()  # 4:50 PM
end_time = datetime.strptime("17:40", "%H:%M").time()    # 5:40 PM

# Create a new KML object and set the document name
kml = simplekml.Kml()
kml.document.name = "SPEED DATA - P2000412780-13.9.2020-Location & Travel-Cached Locations"

# Loop through each row in the DataFrame and filter based on the time
for index, row in df.iterrows():
    # Parse the timestamp to a datetime object
    timestamp_str = row['Timestamp Date/Time - UTC+10:00 (d/MM/yyyy)']
    timestamp_dt = datetime.strptime(timestamp_str, "%d/%m/%Y %I:%M:%S.%f %p")
    
    # Extract the time part and check if it falls within the specified range
    current_time = timestamp_dt.time()
    if start_time <= current_time <= end_time:
        # Convert speed from m/s to km/h if the speed is greater than 0
        if pd.notna(row['Speed (m/s)']) and row['Speed (m/s)'] > 0:
            speed_kmh = row['Speed (m/s)'] * 3.6  # Convert m/s to km/h
            speed_kmh_display = round(speed_kmh, 1)  # Round to 1 decimal place for display
        else:
            continue  # Skip this row if speed is -1, 0, or NaN
        
        # Format the timestamp to ISO 8601 format for KML (e.g., "2020-09-13T14:30:00Z")
        iso_timestamp = timestamp_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Create a point for each row that falls within the time range and has a valid speed
        pnt = kml.newpoint()
        
        # Set the name as the speed in km/h
        pnt.name = f"{speed_kmh_display} km/h"
        print(f"\nCreating point {index + 1}:")
        print(f"Speed (Name): {pnt.name}")
        
        # Set the coordinates (longitude, latitude)
        pnt.coords = [(row['Longitude'], row['Latitude'])]
        print(f"Coordinates: Longitude = {row['Longitude']}, Latitude = {row['Latitude']}")
        
        # Add a TimeStamp element for each point to enable the time slider in Google Earth
        pnt.timestamp.when = iso_timestamp

        # Construct the description field (optional, you can leave it empty or add relevant info)
        full_time = timestamp_dt.strftime("%I:%M:%S %p").lstrip("0")  # Remove leading zero in full time
        full_date = timestamp_dt.strftime("%d/%m/%Y")  # Format the date as DD/MM/YYYY
        description = (
            f"Date: {full_date}\n"
            f"Full Time: {full_time}\n"
            f"Speed: {speed_kmh_display} km/h\n"
            f"Location: {row['Location'] if pd.notna(row['Location']) else 'N/A'}"
        )
        pnt.description = description
        print("Description:")
        print(description)

# Save the KML file to the specified path
kml.save(output_file)
print(f"\nKML file '{output_file}' created successfully with filtered speed data.")


#DISPLAY SPEED YAAK