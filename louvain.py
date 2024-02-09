import pandas as pd
import networkx as nx
import community  # Louvain community detection
import random
import numpy as np
import matplotlib.pyplot as plt
import os

# Set a fixed seed for reproducibility
seed_value = 2
random.seed(seed_value)
np.random.seed(seed_value)

# Set the path to the folder containing CSV files
folder_path = '/home/morteza/Desktop/Alireza/Dataset/data/CallGraph/data/s/'
folder_path1 = '/home/morteza/Desktop/Alireza/Dataset/data/CallGraph/data/s/plot_result'
# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Loop through each CSV file
for csv_file in csv_files:
    # Construct the full path to the CSV file
    csv_file_path = os.path.join(folder_path, csv_file)

    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Create a directed graph using NetworkX
    G = nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph())

    # Convert the directed graph to an undirected graph
    G_undirected = G.to_undirected()

    # Apply Louvain community detection
    partition = community.best_partition(G_undirected, random_state=seed_value)

    # Calculate modularity score
    modularity_score = community.modularity(partition, G_undirected)

    # Add the community information to the DataFrame
    df['community'] = df['source'].map(partition)

    # Calculate coverage
    coverage = len(set(partition.values())) / len(G_undirected.nodes())

    # Calculate density
    density = nx.density(G)

    # Calculate connectivity metrics
    avg_degree = np.mean(list(dict(G.degree()).values()))
    avg_clustering = nx.average_clustering(G)

    # ... (other connectivity metrics can be added as needed)

    # Create a new DataFrame for the output format
    output_df = pd.DataFrame(columns=['timestamp', 'service', 'node', 'community', 'traceid'])

    # Add rows to the new DataFrame for 'source'
    output_df['time'] = df['timestamp']
    output_df['service'] = df['service']
    output_df['node'] = df['source']
    output_df['community'] = df['community']
    output_df['traceid'] = df['traceid']

    # Append rows to the new DataFrame for 'target'
    target_rows = pd.DataFrame(columns=['time', 'service', 'node', 'community', 'traceid'])
    target_rows['time'] = df['timestamp']
    target_rows['service'] = df['service']
    target_rows['node'] = df['target']
    target_rows['traceid'] = df['traceid']
    target_rows['community'] = df['target'].map(partition)
    output_df = pd.concat([output_df, target_rows])

    # Save the new DataFrame to a CSV file
    output_csv_path = os.path.join(folder_path1, f'{csv_file.replace("_output", "_result")}')
    output_df.to_csv(output_csv_path, index=False)

    # Print the metrics
    print(f"Number of Classes: {len(set(partition.values()))}")
    print(f"Modularity Score: {modularity_score}")
    print(f"Coverage: {coverage}")
    print(f"Density: {density}")
    print(f"Average Degree: {avg_degree}")
    print(f"Average Clustering Coefficient: {avg_clustering}")

    # ... (print other connectivity metrics if needed)

    # Create a layout for the graph
    layout = nx.spring_layout(G_undirected)

    # Draw the graph with nodes colored by community
    plt.figure(figsize=(12, 8))
    nx.draw(G_undirected, pos=layout, node_color=list(partition.values()), cmap=plt.cm.RdYlBu, node_size=50, with_labels=False)
    plt.title('Graph with Louvain Communities')

    # Add labels for nodes
    node_labels = {node: node for node in G_undirected.nodes()}
    nx.draw_networkx_labels(G_undirected, pos=layout, labels=node_labels, font_size=8, font_color='black')

    plt.title('Graph with Louvain Communities')

    # Add a text annotation for the service name at the top center of the plot
    service_name = df['service'].iloc[0]  # Assuming all rows have the same service name
    plt.annotate(service_name, xy=(0.5, 1.05), xycoords='axes fraction', ha='center', va='center', fontsize=12, color='black')

    # Save the plot as an image (adjust the filename as needed)
    plot_filename = os.path.join(folder_path1, f'{csv_file.replace("_output", "_plot")}.png')
    plt.savefig(plot_filename)


