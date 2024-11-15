import matplotlib.pyplot as plt
import contextily as cx
import networkx as nx
import pandas as pd
import osmnx as ox
import random
import json
import geopandas as gpd
import numpy as np
import itertools

import overpass
from shapely.geometry import Polygon, LineString, Point
import overpy
from osmapi import OsmApi

# Define the bounding box for the area of interest
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

def plot_rerouted_paths(rerouted_paths):
    """Plot the rerouted paths on a map."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot each path
    for path in rerouted_paths:
        # Get the coordinates of the path
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        for edge in path_edges:
            # Get the geometry of the edge
            if edge in graph_of_area.edges:
                x, y = zip(*[(graph_of_area.nodes[edge[0]]['x'], graph_of_area.nodes[edge[0]]['y']),
                              (graph_of_area.nodes[edge[1]]['x'], graph_of_area.nodes[edge[1]]['y'])])
                ax.plot(x, y, color='blue', linewidth=2)

    # Set the limits and labels
    ax.set_xlim(120.95226, 121.12186)
    ax.set_ylim(14.54603, 14.64106)
    ax.set_title("Rerouted Paths")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Add a basemap
    cx.add_basemap(ax, crs=ox.projected.crs_from_epsg(4326), source=cx.providers.Stamen.Terrain)

    plt.show()

def get_reroute(G_sub, shortest_paths_between_closest_nodes):
    rerouted_sub_graph_lst = []
    for path in shortest_paths_between_closest_nodes:
        rerouted_sub_graph_lst.append(graph_of_area.subgraph(path))
    
    rerouted_sub_graph = nx.compose(G_sub, nx.compose_all(rerouted_sub_graph_lst))
    
    # Convert to GeoDataFrames
    gdf_edges = ox.graph_to_gdfs(rerouted_sub_graph, nodes=False)
    
    # Plot the rerouted paths
    plot_rerouted_paths(shortest_paths_between_closest_nodes)

    return gdf_edges

# Example usage
if __name__ == "__main__":
    # Example of how to use the functions
    G = graph_of_area.copy()
    G_sub = subgraph.copy()
    num_nodes_to_delete = 5
    deleted_nodes = get_random_lst_of_nodes(G_sub, num_nodes_to_delete)
    shortest_paths = get_lst_of_rerouted_paths(G, G_sub, deleted_nodes)
    gdf_edges = get_reroute(G_sub, shortest_paths)