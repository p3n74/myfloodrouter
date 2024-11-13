import osmnx as ox
import networkx as nx
import folium
import json

place_name = "Manila, Philippines"
graph = ox.graph_from_place(place_name, network_type="drive")


origin_node = list(graph.nodes())[0] 
destination_node = list(graph.nodes())[-1]
shortest_path = nx.shortest_path(graph, origin_node, destination_node, weight='length')


route_latlongs = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path]

midpoint = route_latlongs[len(route_latlongs) // 2]
map_folium = folium.Map(location=midpoint, zoom_start=14, tiles='https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}', attr='Google', API_key='YOUR_GOOGLE_MAPS_API_KEY')


folium.PolyLine(route_latlongs, color="blue", weight=5, opacity=0.8).add_to(map_folium)

folium.Marker(location=route_latlongs[0], popup="Start", icon=folium.Icon(color="green")).add_to(map_folium)
folium.Marker(location=route_latlongs[-1], popup="End", icon=folium.Icon(color="red")).add_to(map_folium)


map_folium.save("map_with_google.html")

edges = ox.utils_graph.get_route_edge_attributes(graph, shortest_path)


street_names = []
for edge in edges:

    street = edge.get('name', 'Unnamed road')
    street_names.append(street)


unique_streets = list(dict.fromkeys(street_names))

streets_json = {
    "route": unique_streets
}
with open("streets_route.json", "w") as json_file:
    json.dump(streets_json, json_file, indent=4)
