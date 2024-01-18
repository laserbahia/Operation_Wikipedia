import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

central_topic = "Python Programming"
G.add_node(central_topic)

related_topics = ["Data Structures", "Algorithms", "Object-Oriented Programming", "Functional Programming", "Libraries"]
G.add_nodes_from(related_topics)

G.add_edges_from([(central_topic, topic) for topic in related_topics])

# Set node labels
node_labels = {node: node for node in G.nodes()}
nx.set_node_attributes(G, node_labels, "label")

# Set graph layout
pos = nx.spring_layout(G)

# Draw the graph
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos)

# Show the plot
plt.show()