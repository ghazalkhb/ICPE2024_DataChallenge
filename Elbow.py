import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# Set the path to the folder containing CSV files
folder_path = '/home/morteza/Desktop/Alireza/Dataset/data/CallGraph/data/service1/'

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Dictionary to store graphs and their corresponding nodes
graph_nodes = {}

# Loop through each CSV file
for csv_file in csv_files:
    # Construct the full path to the CSV file
    csv_file_path = os.path.join(folder_path, csv_file)

    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Create a graph from the DataFrame
    G = nx.from_pandas_edgelist(df, 'source', 'target')

    # Store the graph and its nodes in the dictionary
    graph_nodes[csv_file] = list(G.nodes)

# Extract features or similarity measures for clustering
# Example: You can use the number of nodes and edges as features
graph_features = {graph: (len(nodes), G.number_of_edges()) for graph, nodes in graph_nodes.items()}

# Convert features to a Pandas DataFrame
features_df = pd.DataFrame.from_dict(graph_features, orient='index', columns=['num_nodes', 'num_edges'])

# Apply the elbow method to find the optimal number of clusters
distortions = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(features_df)
    distortions.append(kmeans.inertia_)

folder_path1 = '/home/morteza/Desktop/Alireza/Dataset/data/CallGraph/data/service1/elbow'
    
# Plot the elbow curve
plt.plot(range(1, 11), distortions, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Distortion')
plt.title('Elbow Method for Optimal Number of Clusters')

# Save the plot as an image (adjust the filename as needed)
plot_filename = os.path.join(folder_path1, f'{csv_file.replace("_output", "_plot")}.png')
plt.savefig(plot_filename)


