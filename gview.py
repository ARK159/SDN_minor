import networkx as nx
import matplotlib.pyplot as plt
import math
def read_file(file):
    with open('gml','r') as file:
        lines=file.readlines()
    return lines


def haversine_distance(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return abs(rad * c)




file_data=read_file('gml')
graph=nx.parse_gml(file_data)

pos = nx.spring_layout(graph) 
nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=800, font_size=10, font_color='black', font_weight='bold', edge_color='gray')
plt.show()

