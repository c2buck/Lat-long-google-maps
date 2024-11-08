import os
import pandas as pd
import simplekml
from datetime import datetime, timedelta

# Define the base directory path
base_directory = "/mnt/c/Users/c2buc/Downloads/"

# Prompt for the file name only
file_name = input("Please enter the name of the CSV file (e.g., 'XXXX.csv'): ")

# Prompt for additional text to add to the output file name
output_suffix = input("Enter additional text to add to the output filename (e.g., 'Filtered', 'Accuracy_Only'): ")

# Prompt for the accuracy threshold
accuracy_threshold = float(input("Enter the accuracy threshold in meters (e.g., '100' for filtering points below 100 meters): "))

# Construct the full path by joining the base directory and the file name
input_file = os.path.join(base_directory, file_name)

# Check if the file exists
if not os.path.isfile(input_file):
    print(f"Error: The file '{input_file}' does not exist. Please check the file name and try again.")
    exit()

# Generate the output file name with the suffix
output_filename = f"{os.path.splitext(file_name)[0]}_{output_suffix}.kml"
output_file = os.path.join(base_directory, output_filename)

# Print statements to confirm the paths being used
print(f"Opening CSV file: {input_file}")
print(f"Saving KML file to: {output_file}")

# Load the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Filter rows where 'Accuracy (m)' is below the user-defined threshold
df = df[df['Accuracy (m)'] < accuracy_threshold]

# Print the first few rows to confirm data is loaded and filtered correctly
print(f"Data loaded and filtered from CSV (Accuracy < {accuracy_threshold} m):")
print(df.head())

# Create a new KML object and set the document name
file_name_without_extension = os.path.splitext(file_name)[0]
kml = simplekml.Kml()
kml.document.name = f"{output_suffix} - Filtered Locations (Accuracy < {accuracy_threshold} m) - {file_name_without_extension}"

# Loop through each row in the filtered DataFrame
for index, row in df.iterrows():
    # Parse the timestamp to a datetime object
    timestamp_str = row['Timestamp Date/Time - UTC+10:00 (d/MM/yyyy)']
    timestamp_dt = datetime.strptime(timestamp_str, "%d/%m/%Y %I:%M:%S.%f %p")

    # Define start and end times for TimeSpan
    start_time = timestamp_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = (timestamp_dt + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")  # Set end time as 1 hour later

    # Create a point for each row
    pnt = kml.newpoint()

    # Set a TimeStamp for the point
    pnt.timestamp.when = start_time

    # Set the name as the accuracy value without decimals
    accuracy_name = int(row['Accuracy (m)']) if pd.notna(row['Accuracy (m)']) else "N/A"
    pnt.name = f"{accuracy_name} m"
    print(f"\nCreating point {index + 1}:")
    print(f"Accuracy (Name): {pnt.name}")

    # Set the coordinates (longitude, latitude)
    pnt.coords = [(row['Longitude'], row['Latitude'])]
    print(f"Coordinates: Longitude = {row['Longitude']}, Latitude = {row['Latitude']}")

    # Set icon and label style
    pnt.style.iconstyle.scale = 0.5  # Set icon size to 0.5
    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png'  # Red pin icon
    pnt.style.labelstyle.color = simplekml.Color.white  # Set label color to white (#ffffff)
    pnt.style.labelstyle.scale = 1.0  # Set label size to 1.0

    # Construct the description field
    full_accuracy = row['Accuracy (m)'] if pd.notna(row['Accuracy (m)']) else "N/A"
    full_time = timestamp_dt.strftime("%I:%M:%S %p").lstrip("0")
    full_date = timestamp_dt.strftime("%d/%m/%Y")
    description = (
        f"Date: {full_date}\n"
        f"Full Time: {full_time}\n"
        f"Accuracy: {full_accuracy} m\n"
        f"Altitude: {int(row['Altitude (m)']) if pd.notna(row['Altitude (m)']) else 'N/A'} m\n"
        f"Altitude Accuracy: {int(row['Altitude Accuracy (m)']) if pd.notna(row['Altitude Accuracy (m)']) else 'N/A'} m\n"
        f"Direction: {int(row['Direction']) if pd.notna(row['Direction']) else 'N/A'}°\n"
        f"Speed: {int(row['Speed (m/s)']) if pd.notna(row['Speed (m/s)']) else 'N/A'} m/s\n"
        f"Source: {row['Source'] if pd.notna(row['Source']) else 'N/A'}\n"
        f"Location: {row['Location'] if pd.notna(row['Location']) else 'N/A'}"
    )
    pnt.description = description
    print("Description:")
    print(description)

# Save the KML file to the specified output folder
kml.save(output_file)
print(f"\nKML file '{output_file}' created successfully.")
