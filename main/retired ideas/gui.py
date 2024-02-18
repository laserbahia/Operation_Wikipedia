import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# Read the central topic from article_to_be_searched.txt
with open("main/article_to_be_searched.txt", "r") as f1:
    article_to_be_searched = f1.read().strip()

# Read the related topics from linked_articles.txt and remove any empty lines
with open("main/linked_articles.txt", "r") as f2:
    related_topics_raw = [line.strip() for line in f2]
    related_topics_for_central_topic = [topic for topic in related_topics_raw if topic]


# Extract the central_topic and related_topics from the articles list
central_topic_string = article_to_be_searched
central_topic = article_to_be_searched

remaining_articles = related_topics_for_central_topic
central_topic = article_to_be_searched
G.add_node(central_topic)

related_topics = related_topics_for_central_topic
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