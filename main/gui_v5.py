import pickle
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Load all the necessary information from the files
with open("main/txt_files/article_to_be_searched.txt", "r") as f1:  # Load central topic
    central_topic = f1.read().strip()
with open("main/txt_files/linked_linked_articles.pkl", "rb") as f2:  # Load how to link the stuff
    links_of_linked_articles = pickle.load(f2)
    print(links_of_linked_articles)
with open("main/txt_files/linked_articles.txt", "r") as f3:  # Read the related topics from linked_articles.txt and remove any empty lines
    related_topics_raw = [line.strip() for line in f3]
    important = [topic for topic in related_topics_raw if topic]
with open("main/txt_files/linkes_in_links.pkl","rb") as f4:
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
for source, targets in links_in_links.items():
    for target in targets:
        if target in links_of_linked_articles:  # Check if target is in links_of_linked_articles
            for link_target in links_of_linked_articles[target][0]:
                G.add_edge(target, link_target)

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

# Plot the graph
pos = nx.spring_layout(G, k=2)
nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=colors, font_size=10, font_weight='bold')
plt.title("Wikipedia Article Network")
plt.show()
