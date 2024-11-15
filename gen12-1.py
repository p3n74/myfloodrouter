# myfloodrouter/gen12-1.py

import json
import geopandas as gpd

def generate_unique_streets_json():
    # Load the GeoJSON files
    edges = gpd.read_file('rerouted_edges.geojson')
    nodes = gpd.read_file('rerouted_nodes.geojson')

    # Print the columns to check for the correct name
    print("Columns in nodes GeoDataFrame:", nodes.columns)

    # Check if 'name' column exists in nodes
    if 'name' in nodes.columns:
        unique_streets = []
        for name in nodes['name']:
            if name is None:  # Check for null (None in Python)
                # If name is null, create a new name
                previous_street_name = "Unnamed Street"  # Default name if no previous name is available
                new_name = f"{previous_street_name} service road"
                unique_streets.append(new_name)
            else:
                unique_streets.append(name)

        # Define the desired order
        desired_order = ["Valenzuela Street", "Maysilo Circle", "Boni Avenue", "P. Sanchez Street", "P. Sanchez Street service road"]

        # Sort unique streets based on the desired order
        unique_streets = sorted(set(unique_streets), key=lambda x: desired_order.index(x) if x in desired_order else len(desired_order))

    else:
        raise KeyError("The 'name' column does not exist in the nodes GeoDataFrame.")

    # Write the unique streets to a JSON file
    with open('map2streets.json', 'w') as json_file:
        json.dump(unique_streets, json_file)

# Call the function to generate the JSON file
generate_unique_streets_json()