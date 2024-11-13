import osmnx as ox
import folium

# Define the list of streets (you can adjust this to include all the streets needed)
streets = [
    "España, Manila, Philippines",
    "M. dela Fuente, Manila, Philippines",
    "España Boulevard, Manila, Philippines",
    "Vicente Cruz Street, Manila, Philippines",
    "G. Tuazon Street, Manila, Philippines",
    "Balic-Balic, Manila, Philippines",
    "G. Tuazon Street, Manila, Philippines",  # Return leg
    "M. dela Fuente, Manila, Philippines"    # Return leg
]

# Initialize a list to store the coordinates of each street
coordinates = []

# Fetch coordinates of each street from OSM using geocode
for street in streets:
    location = ox.geocode(street)
    coordinates.append(location)

# Create a map centered around the midpoint of the route
midpoint = [(coordinates[0][0] + coordinates[-1][0]) / 2, (coordinates[0][1] + coordinates[-1][1]) / 2]
map_folium = folium.Map(location=midpoint, zoom_start=14)

# Plot the route on the map as a PolyLine
folium.PolyLine(coordinates, color="blue", weight=5, opacity=0.8).add_to(map_folium)

# Add markers for each street in the route
for i, coord in enumerate(coordinates):
    folium.Marker(location=coord, popup=streets[i], icon=folium.Icon(color="green" if i == 0 else "red")).add_to(map_folium)

# Save the map to an HTML file
map_folium.save("streets_route_map.html")

print("Map has been saved as 'streets_route_map.html'.")
