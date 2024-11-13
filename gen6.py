import folium
import osmnx as ox
import json
import overpy

# Example: Define the coordinates for jeepney route (start and end points)
start_coords = (14.5995, 120.9842)  # Example: Metro Manila, Philippines
end_coords = (14.6231, 121.0174)   # Example: Another location

# Fetch the map from OpenStreetMap for the area
place_name = "Metro Manila, Philippines"  # Customize to your area of interest
graph = ox.graph_from_place(place_name, network_type='all')

# Plot the route using Folium
map_center = [14.5995, 120.9842]  # Set the map center
route_map = folium.Map(location=map_center, zoom_start=12)

# Convert graph to GeoDataFrame to plot the route
nodes, edges = ox.graph_to_gdfs(graph)

# Overpass API query to fetch the T307 jeepney route
# Query to find routes tagged as 'bus' around the start location (you can modify the query as needed)
api = overpy.Overpass()
result = api.query("""
    way["route"="bus"](around:1000,14.5995,120.9842);
    (._;>;);
    out body;
""")

# Check if we have any results from the query
if result.ways:
    print(f"Found {len(result.ways)} bus routes.")
else:
    print("No bus routes found. Check your query.")

# Extract the coordinates from the Overpass query result
route_coords = []
for way in result.ways:
    for node in way.nodes:
        route_coords.append([node.lat, node.lon])

# Check if the route_coords list is populated
if not route_coords:
    print("Error: route_coords is empty. No valid coordinates were found.")
else:
    print(f"Found {len(route_coords)} coordinates for the route.")

# Plot the jeepney route on the map if coordinates are available
if route_coords:
    folium.PolyLine(route_coords, color='blue', weight=4.5, opacity=0.7).add_to(route_map)

    # Add markers for start and end points
    folium.Marker(location=route_coords[0], popup='Start').add_to(route_map)
    folium.Marker(location=route_coords[-1], popup='End').add_to(route_map)

    # Save the map as an HTML file (Overwriting the previous map)
    route_map.save("jeepney_route_map.html")

    # Fetch street names along the route using osmnx
    street_names = []
    for node in graph.nodes:
        # Retrieve the nearest OSM street name for each node in the route
        for u, v, data in graph.edges(node, data=True):
            if 'name' in data:
                street_names.append(data['name'])

    # Remove duplicates and create JSON
    street_names = list(set(street_names))

    # Save the street names in JSON format (Overwriting the previous JSON)
    with open("street_names.json", "w") as f:
        json.dump(street_names, f, indent=4)

    print("Map and JSON have been saved successfully.")
else:
    print("No route coordinates available to plot.")
