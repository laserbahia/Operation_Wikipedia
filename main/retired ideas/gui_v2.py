import networkx as nx
import matplotlib.pyplot as plt

# Create an empty graph
G = nx.Graph()

# Read the central topic from article_to_be_searched.txt
with open("main/txt_files/article_to_be_searched.txt", "r") as f1:
    central_topic = f1.read().strip()

# Read the related topics from linked_articles.txt and remove any empty lines
with open("main/txt_files/linked_articles.txt", "r") as f2:
    related_topics_raw = [line.strip() for line in f2]
    related_topics = [topic for topic in related_topics_raw if topic]

# Add nodes for the central topic and related topics
G.add_node(central_topic)
G.add_nodes_from(related_topics)

# Create edges between the central topic and related topics
G.add_edges_from([(central_topic, topic) for topic in related_topics])

# Set node labels (optional)
node_labels = {node: node for node in G.nodes()}
nx.set_node_attributes(G, node_labels, "label")

# Compute the ego graph centered around the central topic
radius = 10  # You can adjust the radius as needed
ego_graph = nx.ego_graph(G, central_topic, radius=radius)

# Set graph layout with increased spacing (adjust k value)
pos = nx.spring_layout(ego_graph, k=1)  # Experiment with different k values

# Draw the ego graph with custom font size
plt.figure(figsize=(14, 12))  # Set desired figure size
nx.draw_networkx_nodes(ego_graph, pos, node_size=1000)
nx.draw_networkx_labels(ego_graph, pos, font_size=8, font_weight="bold", font_color="black")  # Adjust font size and weight here
nx.draw_networkx_edges(ego_graph, pos)

plt.title("Related Topics for: " + central_topic)
plt.show()
