import osmnx as ox
import networkx as nx
import folium

# 1. Download the graph of a small area (Manhattan, New York)
place_name = "Manhattan, New York, USA"
graph = ox.graph_from_place(place_name, network_type="drive")

# 2. Generate the shortest path between two random nodes
origin_node = list(graph.nodes())[0]  # Start node
destination_node = list(graph.nodes())[-1]  # End node
shortest_path = nx.shortest_path(graph, origin_node, destination_node, weight='length')

# 3. Convert the nodes to latitude/longitude coordinates for the shortest path
route_latlongs = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path]

# 4. Create a Folium map using Google Maps tiles
midpoint = route_latlongs[len(route_latlongs) // 2]
map_folium = folium.Map(location=midpoint, zoom_start=14, tiles='https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}', attr='Google', API_key='YOUR_GOOGLE_MAPS_API_KEY')

# 5. Add the shortest path as a line on the map
folium.PolyLine(route_latlongs, color="blue", weight=5, opacity=0.8).add_to(map_folium)

# 6. Add markers for the start and end points
folium.Marker(location=route_latlongs[0], popup="Start", icon=folium.Icon(color="green")).add_to(map_folium)
folium.Marker(location=route_latlongs[-1], popup="End", icon=folium.Icon(color="red")).add_to(map_folium)

# 7. Save the map as an HTML file
map_folium.save("map_with_google.html")
