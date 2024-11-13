import requests
import csv

# Define Overpass API query for streets in Manila
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:csv(::id, name, highway)];
area["name"="Manila"]->.searchArea;
(
  way["highway"](area.searchArea);
);
out body;
"""

# Send the query to Overpass API
response = requests.get(overpass_url, params={'data': overpass_query})

# Check if the response is successful
if response.status_code == 200:
    data = response.text

    # Write the CSV to a file
    with open('manila_streets.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_file.write(data)
    print("CSV file saved successfully.")
else:
    print("Error fetching data from Overpass API.")
