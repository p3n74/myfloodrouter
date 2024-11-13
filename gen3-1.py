import osmnx as ox
import networkx as nx
import folium
import json

# 1. Download the graph of Manila
place_name = "Manila, Philippines"
graph = ox.graph_from_place(place_name, network_type="drive")

# 2. Define approximate start and end locations of the T307 route
start_location = (14.5995, 120.9842)  # Approximate coordinates of a start point (example)
end_location = (14.5550, 120.9890)  # Approximate coordinates of an end point (example)

# Find nearest nodes to these locations in the network
start_node = ox.distance.nearest_nodes(graph, X=start_location[1], Y=start_location[0])
end_node = ox.distance.nearest_nodes(graph, X=end_location[1], Y=end_location[0])

# 3. Generate the shortest path between the start and end nodes
shortest_path = nx.shortest_path(graph, start_node, end_node, weight='length')

# 4. Convert the nodes to latitude/longitude coordinates for the shortest path
route_latlongs = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path]

# 5. Get street names and detailed OSM data along the route
route_details = []
for i in range(len(shortest_path) - 1):
    u = shortest_path[i]
    v = shortest_path[i + 1]
    edge_data = graph.get_edge_data(u, v)
    
    # Get the street name, if available
    street_name = edge_data[0].get('name', 'Unnamed street')
    
    # Get additional OSM data (e.g., highway type, road length)
    osm_data = edge_data[0]
    highway_type = osm_data.get('highway', 'Unknown')
    road_length = osm_data.get('length', 0)
    
    # Store the data in a dictionary
    route_details.append({
        'start_node': u,
        'end_node': v,
        'street_name': street_name,
        'highway': highway_type,
        'length': road_length,
        'coordinates': [(graph.nodes[u]['y'], graph.nodes[u]['x']), (graph.nodes[v]['y'], graph.nodes[v]['x'])]
    })

# 6. Save the data to a JSON file
with open('t307_route_streets.json', 'w') as json_file:
    json.dump(route_details, json_file, indent=4)

# 7. Create a Folium map using Google Maps tiles
midpoint = route_latlongs[len(route_latlongs) // 2]
map_folium = folium.Map(location=midpoint, zoom_start=14, tiles='https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}', attr='Google', API_key='YOUR_GOOGLE_MAPS_API_KEY')

# 8. Add the shortest path as a line on the map
folium.PolyLine(route_latlongs, color="blue", weight=5, opacity=0.8).add_to(map_folium)

# 9. Add markers for the start and end points
folium.Marker(location=route_latlongs[0], popup="Start", icon=folium.Icon(color="green")).add_to(map_folium)
folium.Marker(location=route_latlongs[-1], popup="End", icon=folium.Icon(color="red")).add_to(map_folium)

# 10. Save the map as an HTML file
map_folium.save("t307_jeepney_route_with_streets.html")
