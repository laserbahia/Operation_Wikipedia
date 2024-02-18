import networkx as nx
import matplotlib.pyplot as plt
import pickle

def print_keys_and_values(dictionary, G, central_topic):
    for key, value_list in dictionary.items():
        print("Key:", key)
        G.add_node(key)
        G.add_edge(central_topic, key, color='black', width=2.0)  # Thick and black edge from central topic to key
        for value in value_list:
            print("Value:", value)
            G.add_node(value)  # Add node for each value
            G.add_edge(key, value, color='gray', width=1.0)  # Thin and gray edge from key to value

# Create an empty graph
G = nx.Graph()

# load the central topic from the file
with open("main/txt_files/article_to_be_searched.txt", "r") as f1:
    central_topic = f1.read().strip()


#load dictionary
with open("main/txt_files/linked_linked_articles.pkl","rb") as f2:
    my_dict = pickle.load(f2)
    print(my_dict)

#call main funciton 
print_keys_and_values(my_dict, G, central_topic)

# Compute the ego graph centered around the central topic
radius = 15  # You can adjust the radius as needed
ego_graph = nx.ego_graph(G, central_topic, radius=radius)

# Set graph layout with increased spacing (adjust k value)
pos = nx.spring_layout(ego_graph, k=2.75)  # Experiment with different k values

# Draw the ego graph with custom font size and node size
plt.figure(figsize=(14, 12))  # Set desired figure size
nx.draw_networkx_nodes(ego_graph, pos, node_size=5000, nodelist=[central_topic], node_color='skyblue')  # Increase node size for central topic
nx.draw_networkx_nodes(ego_graph, pos, node_size=1000, nodelist=[node for node in ego_graph.nodes() if node != central_topic], node_color='lightblue')  # Larger node size for keys
nx.draw_networkx_labels(ego_graph, pos, font_size=6, font_weight="bold", font_color="black")  # Adjust font size and weight here
nx.draw_networkx_edges(ego_graph, pos, width=1.0)  # Thicker edges between central topic and keys
nx.draw_networkx_edges(ego_graph, pos, edge_color='gray')  # Gray edges between keys and values

plt.title("Related Topics for: " + central_topic)
plt.show()

