import folium
import geopandas as gpd

# Ask for GeoJSON file names
edges_file = input("Enter the edges GeoJSON file name (e.g., 'rerouted_edges.geojson'): ")
nodes_file = input("Enter the nodes GeoJSON file name (e.g., 'rerouted_nodes.geojson'): ")

# Load GeoJSON files
edges = gpd.read_file(edges_file)
nodes = gpd.read_file(nodes_file)

# Print geometry types
print("Geometry types in 'nodes':")
print(nodes.geometry.geom_type.value_counts())

# Create a Folium map centered around the mean coordinates of the nodes
# If there are no Point geometries, we will center the map based on the first LineString if available
if nodes.geometry.geom_type.isin(['Point']).any():
    center_location = [nodes.geometry.y.mean(), nodes.geometry.x.mean()]
else:
    # If there are no Points, check for LineStrings and use the first one to center the map
    line_coords = nodes[nodes.geometry.geom_type == 'LineString'].geometry.iloc[0].coords
    center_location = [line_coords[0][1], line_coords[0][0]] if line_coords else [0, 0]

m = folium.Map(location=center_location, zoom_start=13)

# Add edges to the map
folium.GeoJson(edges).add_to(m)

# Add nodes to the map
for _, row in nodes.iterrows():
    if row.geometry.geom_type == 'LineString':
        # Add the LineString as a PolyLine
        folium.PolyLine(locations=[(coord[1], coord[0]) for coord in row.geometry.coords], color='blue').add_to(m)
    #

# Save the map to an HTML file
m.save('refined_route_map.html')

print("Map has been created and saved as 'refined_route_map.html'.")