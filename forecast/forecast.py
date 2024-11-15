from ecmwf.opendata import Client
import xarray as xr
import osmnx as ox
import joblib
import typing
import geopandas as gpd
import networkx as nx
import numpy as np

client = Client("ecmwf")
model = joblib.load('forecast/rf-model.joblib')
umap_reducer = joblib.load('forecast/euclidian-umap-reducer.joblib')
dem = xr.open_dataset('forecast/dem.nc')
THRESHOLD = 0.01

flood_hazard_map_5yr = gpd.read_file('forecast/5yr/MetroManila5yr.zip', crs='EPSG:32633')
flood_hazard_map_25yr = gpd.read_file('forecast/25yr/MetroManila25yr.zip', crs='EPSG:32633')
flood_hazard_map_100yr = gpd.read_file('forecast/100yr/MetroManila100yr.zip', crs='EPSG:32633')

risk_levels = [0.25, 0.05, 0.01]
hazard_maps = [flood_hazard_map_5yr, flood_hazard_map_25yr, flood_hazard_map_100yr]

parameters = ['tp']
steps = [i for i in range(24, 48, 3)]

FILENAME = 'forecast/tp-probabilities.grib'

def get_elevation(dem, lat, lon):
    # elevation = dem.interp(lat=lat, lon=lon, method='linear')
    # return elevation['z'].values
    return 0
    
# def retrieve_data(client):
#     client.retrieve(
#         time=0,
#         step=[i for i in range(24, 48, 3)],
#         stream="enfo",
#         type=['pf'],
#         levtype="sfc",
#         param=parameters,
#         target=FILENAME
#     )

def get_hazard_level(lat, lon):
    for hazard_map, risk_level in zip(hazard_maps, risk_levels):
        if hazard_map.to_crs(epsg=4326).geometry.contains(Point(lon, lat))[0] is True:
            return risk_level

def interp_data(data, target_lon, target_lat):
    if target_lon is None or target_lat is None:
        print(f"Warning: target_lon or target_lat is None. Values: lon={target_lon}, lat={target_lat}")
        return None  # or handle this case appropriately
    return data.interp(longitude=target_lon, latitude=target_lat, method='linear')

def transform_to_x(graph, data) -> typing.Generator:
    for node_id, node_data in graph.nodes(data=True):
        lon, lat = (node_data.get('lon'), node_data.get('lat'))
        if lon is None or lat is None:
            print(f"Warning: Node {node_id} has invalid coordinates: lon={lon}, lat={lat}")
            continue  # Skip this node

        if 'tp' in data:
            precipitation_data = data['tp']  # Extract the relevant DataArray
            precipitation = interp_data(precipitation_data, lon, lat)
            if precipitation is not None:
                yield np.array([lat, lon, precipitation.values, get_hazard_level(lat, lon), get_elevation(dem, lat, lon)]), node_id
        else:
            print(f"'tp' key not found in data: {data.keys()}")

def get_flooded_nodes(graph, data) -> typing.Generator:
    transformed_data = list(transform_to_x(graph, data))
    
    # Check if transformed_data is empty
    if not transformed_data:
        print("Warning: No valid nodes to process for flooding.")
        return  # or yield an empty generator if needed

    array = np.array(transformed_data)
    x = array[:, 0]
    node_ids = array[:, 1]
    predictions = model.predict(x)
    predictions = (predictions >= THRESHOLD).astype(int)
    for i, prediction in enumerate(predictions):
        if prediction == 1:
            yield node_ids[0]

def simulate_flooding(graph: nx.Graph, data):
    flooded_nodes = list(get_flooded_nodes(graph, data))
    if not flooded_nodes:
        print("Warning: No nodes were flooded. Returning the original graph.")
        return graph  # Return the original graph if no nodes are flooded
    graph.remove_nodes_from(flooded_nodes)
    return graph



if __name__ == '__main__':
    # retrieve_data(client)
    data = xr.load_dataset(FILENAME, engine='cfgrib')
    graph_path = 'forecast/T307-graph-original.graphml'
    route_graph = ox.io.load_graphml(graph_path)
    for step, group in data.groupby('step'):
        filename_prefix = 'map0-nodes'
        graph = route_graph.copy()
        df_nodes, df_edges = ox.graph_to_gdfs(simulate_flooding(graph, group))
        df_nodes.to_file(filename_prefix + '-' + str(step / 3), driver='GeoJSON')
        