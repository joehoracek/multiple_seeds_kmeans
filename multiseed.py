import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import matplotlib.pyplot as plt
import os

def load_pca(filepath):
    return pd.read_csv(filepath, index_col=0)

def run_kmeans_multiple_seeds(data, k, n_runs= 1000):
#n_runs should be the same as the number of seeds
    unique_clusterings = []
    seen_clusterings = set()
    first_seed_for_cluster = {}  

    for seed in range(n_runs):
        kmeans = KMeans(n_clusters=k, random_state=seed, n_init='auto')
        labels = tuple(kmeans.fit_predict(data))

        # Normalize labels to handle permutations of cluster labels
        label_order = np.argsort([np.mean(data[np.array(labels) == i], axis=0).sum() for i in range(k)])
        relabeled = [label_order.tolist().index(l) for l in labels]
        relabeled = tuple(relabeled)

        if relabeled not in seen_clusterings:
            seen_clusterings.add(relabeled)
            unique_clusterings.append(relabeled)
            first_seed_for_cluster[relabeled] = seed # store first seed 

    return unique_clusterings, first_seed_for_cluster

def plot_and_save_cluster(df, labels, specimen_names, cluster_id):
    plt.figure(figsize=(8, 6))
    
  
    # Dynamically generate colors for clusters
    n_clusters = max(labels) + 1
    cmap = plt.get_cmap("tab10")  # tab10 has 10 colors, can switch to tab20 for more
    cluster_colors = [cmap(i % 10) for i in range(n_clusters)]  # safely cycle colors
    


    colors = [cluster_colors[l] for l in labels]  # map each label to a color

    scatter = plt.scatter(df[:, 0], df[:, 1], c=colors, s=50, edgecolor='k')
    
    # Annotate points with specimen names
    for i, name in enumerate(specimen_names):
        plt.annotate(name, (df[i, 0], df[i, 1]), fontsize=8, alpha=0.7)
    
    plt.title(f'Unique Clustering #{cluster_id}')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.grid(True)
    os.makedirs("cluster_plots", exist_ok=True)
    plt.savefig(f"cluster_plots/cluster_{cluster_id}.png", bbox_inches='tight')
    plt.close()

def write_clusters_to_file(specimen_names, clusterings, output_file="cluster_assignments.txt"):
    with open(output_file, 'w') as f:
        for i, labels in enumerate(clusterings):
            f.write(f"Unique Clustering #{i + 1}:\n")
            for label in sorted(set(labels)):
                f.write(f"  Cluster {label}:\n")
                members = [name for name, l in zip(specimen_names, labels) if l == label]
                for name in members:
                    f.write(f"    {name}\n")
            f.write("\n")

if __name__ == "__main__":
    # Modify these:
    csv_path = "coord-example.csv"  # Your PCA coordinates exported to CSV
    k = 2  # Specify k
    n_seeds = 1000 #this program can run any number of seeds

    df = load_pca(csv_path)
    pca_data = df.to_numpy()
    specimen_names = df.index.tolist()

    unique, first_seeds = run_kmeans_multiple_seeds(pca_data, k, n_runs=n_seeds)
    print(f"Total unique clusterings for k={k} over {n_seeds} seeds: {len(unique)}")

    with open("first_seed_per_unique_clustering.txt", "w") as f:
        for i, labels in enumerate(unique):
            seed = first_seeds[labels]
            f.write(f"Unique Clustering #{i + 1}: first seed = {seed}\n")

####First seed used per unique cluster is provided to assist in reproducibility 


    for i, labels in enumerate(unique):
        plot_and_save_cluster(pca_data, labels, specimen_names, i + 1)

    write_clusters_to_file(specimen_names, unique)










