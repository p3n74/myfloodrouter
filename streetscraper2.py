import requests
import json

# Define the Overpass query to get all streets in Metro Manila, including node IDs
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area["name"="Metro Manila"]->.searchArea;
(
  way["highway"](area.searchArea);
);
out body geom qt;
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
    if 'nodes' not in element:
        continue  # Skip ways without node IDs

    nodes = element['nodes']  # List of node IDs for this way (street)

    if len(nodes) < 2:  # Need at least two nodes to form a road segment
        continue
    
    # Collect coordinates for the way from the node IDs
    for point in element['geometry']:
        coordinates.append([point['lon'], point['lat']])

    street = {
        "start_node": nodes[0],  # The first node in the way
        "end_node": nodes[-1],   # The last node in the way
        "node_ids": nodes,        # Include the list of node IDs
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
