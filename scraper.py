import osmnx as ox
import json

# Define the bounding box for the area of interest
BOUNDING_BOX = (14.64106, 14.54603, 121.12186, 120.95226)

# Load the graph from OSM
graph = ox.graph_from_bbox(bbox=BOUNDING_BOX)

# Get the nodes and edges from the graph
nodes, edges = ox.graph_to_gdfs(graph, nodes=True, edges=True)

# Prepare the data structure for JSON
data = {
    "nodes": [],
    "edges": []
}

# Extract node information
for idx, row in nodes.iterrows():
    node_info = {
        "id": idx,
        "x": row['x'],
        "y": row['y'],
        "street_count": row['street_count'] if 'street_count' in row else None,
        "highway": row['highway'] if 'highway' in row else None
    }
    data["nodes"].append(node_info)

# Extract edge information
for idx, row in edges.iterrows():
    edge_info = {
        "id": idx,
        "source": row['u'],  # Source node ID
        "target": row['v'],  # Target node ID
        "length": row['length'],
        "geometry": row['geometry'].wkt  # Convert geometry to WKT format
    }
    data["edges"].append(edge_info)

# Save the data to a JSON file
with open('t307_route_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("T307 route data has been saved to t307_route_data.json.")