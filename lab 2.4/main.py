from matrix import *
from draw_graph import *
from calculations import *

# Define constants and parameters
n1 = 4
n2 = 2
n3 = 0
n4 = 6
# SEED = 4206

n = n3 + 10

# Coefficients for graph generation
k1 = 1.0 - n3*0.01 - n4*0.01 - 0.3
k2 = 1.0 - n3*0.005 - n4*0.005 - 0.27

# Function to analyze and print graph properties
def get_graph_info(dir, undir, modified=False):
    in_degrees = get_in_degrees(dir)
    out_degrees = get_out_degrees(dir)
    if not modified:
        # Print adjacency matrices
        print_matrix(dir, "Directed graph")
        print_matrix(undir, "Undirected graph")
        
        # Analyze degrees
        undir_degrees = get_undir_degrees(dir)
        print_undir_degrees(undir_degrees)
        
        print_dir_degrees(in_degrees, out_degrees)

        # Check if the graph is regular
        print(f"Graph is regular: {is_regular(undir_degrees)[0] if is_regular(undir_degrees)[0] == False else is_regular(undir_degrees)}")
        
        # Identify isolated and leaf nodes
        isolated, leaf = get_isolated_and_leaf(undir_degrees)
        print(f"Isolated nodes: {isolated}")
        print(f"Leaf nodes: {leaf}")
        print("\n\n")
    else:
        # Print adjacency matrices
        print_matrix(dir, "New directed graph")
        print_matrix(undir, "New undirected graph")

        # Analyze degrees
        print_dir_degrees(in_degrees, out_degrees)



# === Original graph analysis ===
dir = get_dir(n, k1)  # Generate directed graph
undir = get_undir(dir)  # Convert to undirected graph
get_graph_info(dir, undir)

# === Modified graph analysis ===
new_dir = get_dir(n, k2)  # Generate modified directed graph
new_undir = get_undir(new_dir)  # Convert to undirected graph
get_graph_info(new_dir, new_undir, modified=True)

# === Path analysis ===
# Analyze paths of specific lengths
paths_2 = paths_length_2(new_dir)
paths_3 = paths_length_3(new_dir)
print_paths(paths_2, 2)
print_paths(paths_3, 3)

# Compute reachability and strong connectivity
A = reachability_matrix(new_dir)
print_matrix(A, "Reachability matrix")

S = strong_connectivity_matrix(A)
print_matrix(S, "Strong connectivity")

# Identify strongly connected components
components = find_strong_components(S, n)
print("Strong connectivity components:")
for i, comp in enumerate(components):
    print(f"Component {i + 1}: nodes {comp}")

# Generate condensation graph
C = condensation_graph(components, new_dir)
print_matrix(C, "Condensation graph")

# === Draw graphs ===
draw_graph(dir, directed=True)  # Original directed graph
draw_graph(dir, directed=False)  # Original undirected graph
draw_graph(new_dir, directed=True)  # Modified directed graph
draw_graph(C, directed=True)  # Condensation graph