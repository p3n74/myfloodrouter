import requests
import json

# Define the Overpass query to get all streets in Metro Manila
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area["name"="Metro Manila"]->.searchArea;
(
  way["highway"](area.searchArea);
);
out body geom;
"""

# Fetch data from Overpass API
response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()

# Prepare the JSON structure for streets in Metro Manila
streets = []

for element in data['elements']:
    # Skip if there are no coordinates for the element
    if 'geometry' not in element:
        continue
    
    coordinates = []
    for point in element['geometry']:
        coordinates.append([point['lon'], point['lat']])

    street = {
        "start_node": element['id'],  # Using the OSM way ID as the start_node
        "end_node": element['id'],  # Assuming the end node is the same as start node (simplification)
        "street_name": element.get('tags', {}).get('name', 'Unnamed street'),
        "highway": element.get('tags', {}).get('highway', 'unknown'),
        "length": element.get('tags', {}).get('length', 0),  # Length might not always be available
        "coordinates": coordinates
    }

    streets.append(street)

# Save the result to a JSON file
with open('metro_manila_streets.json', 'w') as outfile:
    json.dump(streets, outfile, indent=4)

print("Metro Manila streets data has been saved to 'metro_manila_streets.json'")
