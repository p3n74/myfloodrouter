import json
import folium
import networkx as nx
import re

# Load the rerouted node IDs from the JSON file
with open('rerouted_nodes.json', 'r') as f:
    rerouted_data = json.load(f)
    # Create a list of tuples for connected node pairs
    node_pairs = [(entry['node_id'][0], entry['node_id'][1:]) for entry in rerouted_data]

# Load the GraphML file
G = nx.read_graphml('T307-graph-original.graphml')

# Extract coordinates from nodes
coordinates = {}
for node in G.nodes(data=True):
    node_id = node[0]
    lat = float(node[1].get('y'))  # Latitude
    lon = float(node[1].get('x'))  # Longitude
    coordinates[node_id] = (lon, lat)  # Store as (lon, lat)

# Extract edge geometries based on the LINESTRING data
edge_coordinates = {}
for edge in G.edges(data=True):
    line_string = edge[2].get('geometry')  # Assuming 'geometry' is the key for LINESTRING
    if line_string:
        # Extract coordinates from the LINESTRING format
        coords = re.findall(r'\((.*?)\)', line_string)
        if coords:
            # Split the coordinates and convert to tuples of (lon, lat)
            points = [tuple(map(float, point.split())) for point in coords[0].split(',')]
            edge_coordinates[(edge[0], edge[1])] = points  # Use (source, target) as the key

# Extract the route coordinates based on the node pairs
route_coordinates = []
for start_node, connected_nodes in node_pairs:
    for end_node in connected_nodes:
        if (start_node, end_node) in edge_coordinates:
            route_coordinates.extend(edge_coordinates[(start_node, end_node)])
        elif (end_node, start_node) in edge_coordinates:  # Check for reverse direction
            route_coordinates.extend(edge_coordinates[(end_node, start_node)])

# Check if route coordinates were found
if route_coordinates:
    # Create a folium map centered around the midpoint of the route
    midpoint = [(route_coordinates[0][1] + route_coordinates[-1][1]) / 2, (route_coordinates[0][0] + route_coordinates[-1][0]) / 2]
    map_folium = folium.Map(location=midpoint, zoom_start=14)

    # Plot the route on the map
    folium.PolyLine(locations=[(lat, lon) for lon, lat in route_coordinates], color="blue", weight=5, opacity=0.8).add_to(map_folium)

    # Add markers for each node in the pairs
    for start_node, connected_nodes in node_pairs:
        if start_node in coordinates:
            folium.Marker(location=(coordinates[start_node][1], coordinates[start_node][0]), popup=f"Node ID: {start_node}", icon=folium.Icon(color="green")).add_to(map_folium)
        for end_node in connected_nodes:
            if end_node in coordinates:
                folium.Marker(location=(coordinates[end_node][1], coordinates[end_node][0]), popup=f"Node ID: {end_node}", icon=folium.Icon(color="red")).add_to(map_folium)

    # Save the map to an HTML file
    map_folium.save("refined_route_map.html")
    print("Refined route plotted and saved to refined_route_map.html")
else:
    print("No coordinates found for the specified node pairs.")