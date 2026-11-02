# multiple_seeds_kmeans
Description: This python script allows the user to take the coordinates for a PCA plot and detect multiple cluster solutions with k-means clustering by using hundreds or thousands of different seeds.  It should be noted that the cluster solution is not kept but instead only the unique cluster solutions are kept (e.g. if seed1 and seed2 have the same cluster solution, only one will be kept).  

This python script produces a text document detailing the cluster solutions, images showing the plot for each cluster solution, and a text file containing the first seed that produced each cluster solution (for reproducibility).  

Contents of repository:
- LICENSE.txt
- README.md
- multiseed.py
- ExampleData #example data to run multiseed.py and example output 
	- cluster_assignments.txt #contains cluster solutions
	-- coord-example.csv #an example oordination plot for the user to test multiseed.py
	-- first_seed_per_unique_clustering.txt #shows the first seed that produced each cluster solution
	-- cluster_plots #folder containing image files for each cluster solution
		--- cluster_1.png
		--- cluster_2.png 
