import pandas as pd
import networkx as nx
import community  # Louvain community detection
import random
import numpy as np
import matplotlib.pyplot as plt
import os

# Set a fixed seed for reproducibility
seed_value = 650
random.seed(seed_value)
np.random.seed(seed_value)

# Set the path to the folder containing CSV files
folder_path = '[input folder path]/'
folder_path1 = '[output folder path]'

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Loop through each CSV file
for csv_file in csv_files:
    # Construct the full path to the CSV file
    csv_file_path = os.path.join(folder_path, csv_file)

    df = pd.read_csv(csv_file_path)
    G_undirected = nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.Graph())

    # Apply Louvain community detection
    partition = community.best_partition(G_undirected, random_state=seed_value)
    df['community'] = df['source'].map(partition)

    # Create a new DataFrame for the output format
    output_df = pd.DataFrame(columns=['timestamp', 'service', 'node', 'community', 'traceid'])
    output_df['time'] = df['timestamp']
    output_df['service'] = df['service']
    output_df['node'] = df['source']
    output_df['community'] = df['community']
    output_df['traceid'] = df['traceid']

    target_rows = pd.DataFrame(columns=['time', 'service', 'node', 'community', 'traceid'])
    target_rows['time'] = df['timestamp']
    target_rows['service'] = df['service']
    target_rows['node'] = df['target']
    target_rows['traceid'] = df['traceid']
    target_rows['community'] = df['target'].map(partition)
    output_df = pd.concat([output_df, target_rows])

    output_csv_path = os.path.join(folder_path1, f'{csv_file.replace("_output", "_result")}')
    output_df.to_csv(output_csv_path, index=False)

    # Create a layout for the graph
    layout = nx.spring_layout(G_undirected)

    # Draw the graph with nodes colored by community
    plt.figure(figsize=(12, 8))
    nx.draw(G_undirected, pos=layout, node_color=list(partition.values()), cmap=plt.cm.RdYlBu, node_size=50, with_labels=False)
    plt.title('Graph with Louvain Communities')
    node_labels = {node: node for node in G_undirected.nodes()}
    nx.draw_networkx_labels(G_undirected, pos=layout, labels=node_labels, font_size=8, font_color='black')
    plt.title('Graph with Louvain Communities')

    
    # Save the plot as an image (adjust the filename as needed)
    plot_filename = os.path.join(folder_path1, f'{csv_file.replace("_output", "_plot")}.png')
    plt.savefig(plot_filename)

