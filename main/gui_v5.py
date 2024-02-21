import pickle
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import subprocess
import threading
import keyboard 
import io
import sys

# Define the function to handle the Escape key press
def handle_escape():
    def on_esc_press(e):
        plt.close('all')  # Close all matplotlib windows
        print("Escape key pressed. Exiting...")
        subprocess.Popen([sys.executable, "main.py"]) #opens the main file again, to start over
        
    keyboard.on_press_key("esc", on_esc_press) #call the on_esc_press function, when esc is pressed

# Start listening for the Escape key in a separate thread
threading.Thread(target=handle_escape).start()

# Load all the necessary information from the files
with io.open("txt_files/article_to_be_searched.txt", "r") as f1:  # Load central topic
    central_topic = f1.read().strip()
with open("txt_files/linked_linked_articles.pkl", "rb") as f2:  # Load how to link the stuff
    links_of_linked_articles = pickle.load(f2)
    print(links_of_linked_articles)
with io.open("txt_files/linked_articles.txt", "r") as f3:  # Read the related topics from linked_articles.txt and remove any empty lines
    related_topics_raw = [line.strip() for line in f3]
    important = [topic for topic in related_topics_raw if topic]
with open("txt_files/linkes_in_links.pkl","rb") as f4:
    links_in_links=pickle.load(f4)

# Create a directed graph
G = nx.DiGraph()

# Add edges from the 'important' nodes
for node in important:
    G.add_edge(central_topic, node)

# Add edges from the 'links_of_linked_articles'
for source, (targets, _) in links_of_linked_articles.items():
    for target in targets:
        G.add_edge(source, target)

# Add edges from the 'links_in_links'
for key in links_in_links:
   values = links_in_links[key]
   for i in range(len(values)):
    for j in range(i+1, len(values)):  # Ensure not to repeat connections
        node1 = values[i]
        node2 = values[j]
        print("Adding edge between: ",node1, node2)
        G.add_edge(node1, node2)

# Compute shortest path lengths from the main article
path_lengths = nx.single_source_shortest_path_length(G, source=central_topic)

# Create a colormap that starts with darker blue and gets progressively lighter
cmap = cm.get_cmap('Blues')  

# Invert the path lengths to make larger values correspond to smaller node sizes
inverted_path_lengths = {node: 1 / (1 + path_lengths[node]) for node in path_lengths}

# Scale the node sizes based on inverted path lengths
node_sizes = [5000 * inverted_path_lengths[node] for node in G.nodes]

# Generate colors based on the inverted path lengths and colormap
colors = [cmap(inverted_path_lengths[node]) for node in G.nodes]

# Generate node positions
pos = nx.spring_layout(G, scale=10)

# Function to check and adjust node positions if necessary
def adjust_node_positions(pos, tol=0.01):
    adjusted_pos = pos.copy()
    for node1, (x1, y1) in pos.items():
        for node2, (x2, y2) in pos.items():
            if node1 != node2 and abs(x1 - x2) < tol and abs(y1 - y2) < tol:
                # Nodes have the same position, adjust one of the positions
                adjusted_pos[node2] = (x2 + np.random.normal(0.5,0.5), y2 + np.random.normal(0.5, 0.5))
    return adjusted_pos

pos_adjusted = adjust_node_positions(pos)

# Draw the graph with adjusted node positions
plt.figure(figsize=(10, 8))
nx.draw(G, pos_adjusted, with_labels=True, node_size=node_sizes, node_color=colors, font_size=10, font_weight='bold',)
plt.title("Wikipedia Article Network")
plt.savefig("graphs_folder/current_graph", dpi=500)
plt.show()
