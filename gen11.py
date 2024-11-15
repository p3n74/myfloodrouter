import folium
import geopandas as gpd

# Load GeoJSON files
edges = gpd.read_file('rerouted_edges.geojson')
nodes = gpd.read_file('rerouted_nodes.geojson')

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
        # Get the first point of the LineString
        coords = list(row.geometry.coords)
        if coords:
            folium.Marker(location=[coords[0][1], coords[0][0]]).add_to(m)
    elif row.geometry.geom_type == 'Point':
        folium.Marker(location=[row.geometry.y, row.geometry.x]).add_to(m)

# Save the map to an HTML file
m.save('refined_route_map.html')

print("Map has been created and saved as 'refined_route_map.html'.")