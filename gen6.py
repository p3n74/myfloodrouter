import folium
import osmnx as ox
import json
import overpy


start_coords = (14.5995, 120.9842)
end_coords = (14.6231, 121.0174) 

place_name = "Metro Manila, Philippines" 
graph = ox.graph_from_place(place_name, network_type='all')


map_center = [14.5995, 120.9842]  # Set the map center
route_map = folium.Map(location=map_center, zoom_start=12)


nodes, edges = ox.graph_to_gdfs(graph)


api = overpy.Overpass()
result = api.query("""
    way["route"="bus"](around:1000,14.5995,120.9842);
    (._;>;);
    out body;
""")

if result.ways:
    print(f"Found {len(result.ways)} bus routes.")
else:
    print("No bus routes found. Check your query.")

route_coords = []
for way in result.ways:
    for node in way.nodes:
        route_coords.append([node.lat, node.lon])

if not route_coords:
    print("Error: route_coords is empty. No valid coordinates were found.")
else:
    print(f"Found {len(route_coords)} coordinates for the route.")

if route_coords:
    folium.PolyLine(route_coords, color='blue', weight=4.5, opacity=0.7).add_to(route_map)

    folium.Marker(location=route_coords[0], popup='Start').add_to(route_map)
    folium.Marker(location=route_coords[-1], popup='End').add_to(route_map)

   
    route_map.save("jeepney_route_map.html")

    street_names = []
    for node in graph.nodes:
 
        for u, v, data in graph.edges(node, data=True):
            if 'name' in data:
                street_names.append(data['name'])

 
    street_names = list(set(street_names))

    with open("street_names.json", "w") as f:
        json.dump(street_names, f, indent=4)

    print("Map and JSON have been saved successfully.")
else:
    print("No route coordinates available to plot.")
