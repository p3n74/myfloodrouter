import json
import folium

# Load the JSON data
with open('metro_manila_streets.json', 'r') as f:
    streets_data = json.load(f)

# Define the list of node IDs
node_ids = [
    264965502,
    29256184,
    188165094,
    1254512972,
    671955931,
    22598208
]

# Extract coordinates for the specified node IDs
coordinates = []
for node in streets_data:
    if node['start_node'] in node_ids or node['end_node'] in node_ids:
        coordinates.extend(node['coordinates'])  # Add all coordinates for the street

# Create a folium map centered around the midpoint of the route
if coordinates:
    # Calculate the midpoint for centering the map
    midpoint = [(coordinates[0][1] + coordinates[-1][1]) / 2, (coordinates[0][0] + coordinates[-1][0]) / 2]
    map_folium = folium.Map(location=midpoint, zoom_start=14)

    # Plot the route on the map
    folium.PolyLine(locations=[(lat, lon) for lon, lat in coordinates], color="blue", weight=5, opacity=0.8).add_to(map_folium)

    # Add markers for each node
    for node_id in node_ids:
        for node in streets_data:
            if node['start_node'] == node_id:
                folium.Marker(location=node['coordinates'][0], popup=f"Node ID: {node_id}", icon=folium.Icon(color="green")).add_to(map_folium)

    # Save the map to an HTML file
    map_folium.save("refined_route_map.html")
    print("Refined route plotted and saved to refined_route_map.html")
else:
    print("No coordinates found for the specified node IDs.")