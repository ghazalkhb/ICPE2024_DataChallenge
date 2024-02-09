import os
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from node2vec import Node2Vec
from sklearn.metrics.pairwise import cosine_similarity

# Set the path to the folder containing CSV files
folder_path = '/home/morteza/Desktop/Alireza/Dataset/data/CallGraph/data/service/'

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Dictionary to store graphs and their corresponding nodes
graph_nodes = {}
graph_embeddings = {}

# Loop through each CSV file
for csv_file in csv_files:
    # Construct the full path to the CSV file
    csv_file_path = os.path.join(folder_path, csv_file)

    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Create a graph from the DataFrame
    G = nx.from_pandas_edgelist(df, 'source', 'target')

    # Store the graph, its nodes, and embeddings in the dictionary
    graph_nodes[csv_file] = list(G.nodes)

    # Create an instance of the Node2Vec class
    node2vec = Node2Vec(G, dimensions=30, walk_length=15, num_walks=100, workers=1)

    # Fit the Node2Vec model to the graph
    model = node2vec.fit(window=10, min_count=1, batch_words=4)

    # Get node embeddings
    node_embeddings = {node: model.wv[node] for node in G.nodes}
    graph_embeddings[csv_file] = node_embeddings

# Define similarity range and initialize count dictionary
similarity_ranges = np.arange(-1.0, 1.01, 0.01)
count_per_range = {r: 0 for r in similarity_ranges}

# Initialize count dictionary for each similarity range
count_per_range = {r: 0 for r in similarity_ranges}

# Calculate similarities between all pairs of graphs
similarities = []

for i, (graph1, emb1) in enumerate(graph_embeddings.items()):
    for graph2, emb2 in list(graph_embeddings.items())[i + 1:]:
        # Avoid duplicate pairs by starting the inner loop from i + 1
        avg_emb1 = np.mean(list(emb1.values()), axis=0)
        avg_emb2 = np.mean(list(emb2.values()), axis=0)
        similarity = cosine_similarity([avg_emb1], [avg_emb2])[0][0]
        similarities.append(similarity)

        # Update counts for each similarity range
        for r in similarity_ranges:
            if similarity >= r:
                count_per_range[r] += 1

# Plot the histogram
plt.bar(count_per_range.keys(), count_per_range.values(), width=0.02)
plt.xlabel('Similarity')
plt.ylabel('Number of Pairs')
plt.title('Similarity Distribution')
plt.show()
    
# Sort similarities and print the most similar graph pairs
k = 5  # Replace 5 with the desired number of most similar graph pairs to display
sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

print("Lowest similarities:")
for (graph1, graph2), similarity in sorted_similarities[:-k]:
    print(f"{graph1} and {graph2} have similarity: {similarity}")
    
print("Highest similarities:")
for (graph1, graph2), similarity in sorted_similarities[:k]:
    print(f"{graph1} and {graph2} have similarity: {similarity}")

