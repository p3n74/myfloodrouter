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

BOUNDING_BOX = (14.80719172, 14.31891701, 121.1424698, 120.9012584) # bounding box as (north, south, east, west)
graph_of_area = ox.graph_from_bbox(bbox=BOUNDING_BOX)

ox.plot_graph(graph_of_area)

gdf_edges = ox.graph_to_gdfs(graph_of_area, nodes=False)

gdf_edges_web_mercator = gdf_edges.to_crs(epsg=3857)

_, ax = plt.subplots(1,1, figsize=(15,15))
gdf_edges_web_mercator.plot(linewidth=.75, ax=ax)
cx.add_basemap(ax=ax, url=cx.providers.CartoDB.Positron)

def get_nodes():
    for result in results:
        for way in result.get_ways():
            for node in way.get_nodes(resolve_missing=True):
                yield node

def get_ways():
    for way in result.get_ways():
        yield LineString(Point(node.lon, node.lat) for node in way.get_nodes(resolve_missing=True))
        
def _get_way_ids(relation_id):
    query = f"""
    relation({relation_id});
    out body;
    """
    
    # Fetch the relation data
    result = api.query(query)
    
    # Check if we got the relation
    if len(result.relations) > 0:
        relation = result.relations[0]  # Access the first relation
    else:
        print('Relation Not Found')
    
    for member in relation.members:
        if type(member) == overpy.RelationWay:
           yield member.ref


def get_way_data(relation_ids):
    results = []
    for relation_id in relation_ids:
        query = f"""
        way(id:{','.join(map(str, list(_get_way_ids(relation_id))))});
        out body;
        """
        result = api.query(query)
        results.append(result)
    return results

def get_nearest_nodes_from(graph, lst_of_ll) -> list:
    for node in lst_of_ll:
        x = np.float64(node.lon)
        y = np.float64(node.lat)
        nn, _ = tuple(nn_dist for nn_dist in ox.distance.nearest_nodes(graph, x, y, return_dist=True))
        yield nn

def generate_subgraph_from_node_lst(graph, node_lst) -> nx.Graph:
    SG = graph.__class__()
    SG.add_nodes_from((n, graph.nodes[n]) for n in node_lst)
    if SG.is_multigraph():
        SG.add_edges_from(
            (n, nbr, key, d)
            for n, nbrs in graph.adj.items()
            if n in node_lst
            for nbr, keydict in nbrs.items()
            if nbr in node_lst
            for key, d in keydict.items()
        )
    else:
        SG.add_edges_from(
            (n, nbr, d)
            for n, nbrs in graph.adj.items()
            if n in node_lst
            for nbr, d in nbrs.items()
            if nbr in node_lst
        )
    SG.graph.update(graph.graph)
    return SG

def plot_graph(graph):
    subgraph_edges = ox.graph_to_gdfs(graph, nodes=False)
    _, ax = plt.subplots(figsize=(12, 12))
    subgraph_edges = subgraph_edges.to_crs(epsg=3857)
    subgraph_edges.plot(ax=ax, edgecolor='blue')
    cx.add_basemap(ax=ax, source=cx.providers.CartoDB.Positron)
    ax.set_axis_off()
    
    api = overpy.Overpass()
relation_id_lst = [
    11246071
]

results = get_way_data(relation_id_lst)

for result in results:
    for way in result.get_ways():
        way.get_nodes(resolve_missing=True)
        
node_lst = list(get_nearest_nodes_from(graph_of_area, get_nodes()))

subgraph = generate_subgraph_from_node_lst(graph_of_area, node_lst)

def save_graph_as_geojson(graph, filename):
    # Convert nodes and edges to GeoDataFrames
    gdf_nodes = ox.graph_to_gdfs(graph, nodes=True, edges=False)
    gdf_edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

    # Save to GeoJSON
    gdf_nodes.to_file(filename + '_nodes.geojson', driver='GeoJSON')
    gdf_edges.to_file(filename + '_edges.geojson', driver='GeoJSON')

# Save the subgraph as GeoJSON files
save_graph_as_geojson(subgraph, 'subgraph2')