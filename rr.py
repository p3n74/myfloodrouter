import matplotlib.pyplot as plt
import contextily as cx
import networkx as nx
import pandas as pd
import osmnx as ox
import random
import json
import geopandas as gpd
import numpy as np
import random
import itertools


import overpass
from shapely.geometry import Polygon, LineString, Point
import overpy
from osmapi import OsmApi


BOUNDING_BOX = (14.64106, 14.54603, 121.12186, 120.95226)
graph_of_area = ox.graph_from_bbox(bbox=BOUNDING_BOX)

subgraph = ox.io.load_graphml('T307-graph-original.graphml')


def get_nearest_node_and_delete_it(node_id, graph, x, y):
    graph.remove_node(node_id)
    return get_nearest_node(graph, x, y)


def get_nearest_node(graph, x, y):
    nn, _ = tuple(nn_dist for nn_dist in ox.distance.nearest_nodes(graph.copy(), x, y, return_dist=True))
    return nn


def get_random_lst_of_nodes(graph, num_nodes_to_delete):
    random_nodes = []
    counter = 0
    while True:
        if counter == num_nodes_to_delete:
            break
        node = random.choice(list(graph.nodes))
        if len(list(graph.neighbors(node))) < 2:
            continue
        else:
            random_nodes.append(node)
            counter += 1
    return random_nodes


def get_lst_of_rerouted_paths(G, G_sub, deleted_nodes):
    shortest_paths_between_closest_nodes = []
    for node_id in deleted_nodes:
        try:
            if len(neighbors := list(G_sub.neighbors(node_id))) < 2:
                continue
        except nx.NetworkXError:
            continue
        else:
            G.remove_node(node_id)
            G_sub.remove_node(node_id)
            try:
                shortest_path = nx.shortest_path(G, source=neighbors[0], target=neighbors[1])
                print(shortest_path)
                shortest_paths_between_closest_nodes.append(shortest_path)
                existing_nodes = set(shortest_path).intersection(G_sub.nodes)
                g = nx.articulation_points(nx.MultiGraph(nx.compose(graph_of_area.subgraph(shortest_path), G_sub)))
                exclude = existing_nodes.intersection(g)
                print(exclude)
                if len(existing_nodes) > 2:
                    G_sub.remove_nodes_from(list(existing_nodes - exclude))
            except nx.NetworkXNoPath:
                continue
    return shortest_paths_between_closest_nodes


def get_reroute(G_sub, shortest_paths_between_closest_nodes):
    rerouted_sub_graph_lst = []
    for path in shortest_paths_between_closest_nodes:
        rerouted_sub_graph_lst.append(graph_of_area.subgraph(path))
    rerouted_sub_graph = nx.compose(G_sub, nx.compose_all(rerouted_sub_graph_lst))
    return ox.graph_to_gdfs(rerouted_sub_graph, nodes=False)

# Example usage to create a JSON file
G = graph_of_area.copy()
G_sub = subgraph.copy()
num_nodes_to_delete = 5
deleted_nodes = get_random_lst_of_nodes(G_sub, num_nodes_to_delete)
shortest_paths = get_lst_of_rerouted_paths(G, G_sub, deleted_nodes)
rerouted_graph = get_reroute(G_sub, shortest_paths)

# Extract node IDs from the rerouted graph
node_ids = list(rerouted_graph.index)  # Assuming the first element is the GeoDataFrame

# Format the data as a list of dictionaries
formatted_data = [{"node_id": node_id} for node_id in node_ids]

# Save to a JSON file
with open('rerouted_nodes.json', 'w') as json_file:
    json.dump(formatted_data, json_file, indent=4)



# G = graph_of_area.copy()
# G_sub = subgraph.copy()
# num_nodes_to_delete = 5
# deleted_nodes = get_random_lst_of_nodes(G_sub, num_nodes_to_delete)
# print(deleted_nodes)