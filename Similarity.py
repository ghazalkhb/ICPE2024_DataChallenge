import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from sklearn.metrics import silhouette_score


# Set the path to the folder containing CSV files
folder_path = '[folder Path]'
# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Dictionary to store graphs and their corresponding nodes
graph_nodes = {}

# Loop through each CSV file
for csv_file in csv_files:
    csv_file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(csv_file_path)

    # Create a graph from the DataFrame
    G = nx.from_pandas_edgelist(df, 'source', 'target')
    graph_nodes[csv_file] = list(G.nodes)

# Extract features or similarity measures for clustering
graph_features = {graph: (len(nodes), G.number_of_edges()) for graph, nodes in graph_nodes.items()}

# Convert features to a Pandas DataFrame
features_df = pd.DataFrame.from_dict(graph_features, orient='index', columns=['num_nodes', 'num_edges'])

# Apply K-means clustering
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
clusters = kmeans.fit_predict(features_df)

# Evaluate K-means clustering
silhouette_avg = silhouette_score(features_df, clusters)

print(f"Silhouette Score: {silhouette_avg}")



# Assign cluster labels to graphs
graph_clusters = {graph: cluster for graph, cluster in zip(graph_nodes.keys(), clusters)}

# Print graphs in each cluster
for cluster_id in range(num_clusters):
    graphs_in_cluster = [graph for graph, label in graph_clusters.items() if label == cluster_id]
    print(f"Cluster {cluster_id}: {graphs_in_cluster}")
