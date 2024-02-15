import networkx as nx
import numpy as np
import sys
import math
import pandas as pd
import matplotlib.pyplot as plt


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

def distance(p1, p2,graph,centroids):
    # print(p1[2],'',p1[4])
    lat1=float(p1[2])
    long1=float(p1[4])
    
    lat2=float(p2[2])
    long2=float(p2[4])
    CC_time=0
    # for c in centroids:
    #     CC_distance=haversine_distance(float(c[2]),float(c[4]),lat2,long2)
    #     CC_time+=(CC_distance/(45*1000))
    delay=graph.get_edge_data(p1[0],p2[0])
    
    # print(delay)

    if delay==None:   
        link_label=10*1000
    else:
        
        if 'LinkLabel' in delay.keys():
            link_label=delay['LinkLabel']
            link_label = link_label.replace("<", "")
            if "Gbps" in link_label:
                link_label = float(link_label.replace("Gbps", "")) * 1000  
            elif "Mbps" in link_label:
                link_label = float(link_label.replace("Mbps", ""))
                
        else:
            link_label=155
                
    dist=haversine_distance(lat1,long1,lat2,long2)
    # print(type(link_label),' ',type(CC_time),' ',type(dist))
    return (dist/float(link_label))+(0)

def main(file_data):
    graph=nx.parse_gml(file_data)
    # print("Nodes",graph.nodes(data=True))
    # print("Edges",graph.edges(data=True))
    # print(graph.graph)
    node_list = []
    for node_id, node_data in graph.nodes(data=True):
        temp= [
        node_id,
        node_data.get('Country', ''),
        node_data.get('Latitude', ''),
        node_data.get('Internal', ''),
        node_data.get('Longitude', '')
        ]
        
        node_list.append(temp)
    print(node_list[0],'\n')
    wcss=[]
    for k in range(1,11):
        cent=initialize(node_list,k,graph)
        centroids,labels,wcs=k_means(node_list,k,distance,cent,graph)
        wcss.append(wcs)
    # print(labels)
    plt.plot(range(1, 11), wcss, marker='o')
    plt.title('Elbow Method for Optimal k')
    plt.xlabel('Number of Clusters (k)')    
    plt.ylabel('Within-Cluster Sum of Squares (WCSS) for AARnet')
    plt.show()
    second_derivative = np.diff(np.diff(wcss))
    optimal_k = np.argmax(second_derivative) + 2
    print(optimal_k)
    
    cent=initialize(node_list,2,graph)
    # print(cent)
    centroids,labels,wcs=k_means(node_list,2,distance,cent,graph)
    print(wcs)
    # pos = nx.spring_layout(graph) 
    # nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=800, font_size=10, font_color='black', font_weight='bold', edge_color='gray')
    # plt.show()
    
    print(labels)  
    print(centroids)  
    latitude=[float(c[2]) for c in node_list]
    longitude=[float(c[4]) for c in node_list]
    
    c_latitude=[float(c[2]) for c in centroids]
    c_longitude=[float(c[4]) for c in centroids]
    
    cent_latitude=[float(c[2]) for c in cent]
    cent_longitude=[float(c[4]) for c in cent]
    # print(cent_latitude)
    
    plt.scatter(longitude,latitude,c=labels)
    plt.scatter(c_longitude,c_latitude,color='red') 
    # plt.scatter(cent_longitude,cent_latitude,color='orange')
    
    
    
    
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()






def k_means(X, k, distance_func, centroids, graph, max_iters=1000, tol=1e-4):

    old_labels = np.zeros(len(X))
    
    for _ in range(max_iters):
        
        distances = np.array([[distance_func(x, c, graph, centroids) for c in centroids] for x in X])
        labels = np.argmin(distances, axis=1)

        new_centroids = []

        for i in range(0, k):
            cluster_points = [X[j] for j in range(len(labels)) if i == labels[j]]
            
            if cluster_points:
                lat_mean = np.mean([float(p[2]) for p in cluster_points])
                long_mean = np.mean([float(p[4]) for p in cluster_points])
                new_centroids.append(['', 'Australia', lat_mean, '1', long_mean])

        if (old_labels == labels).all():
            break

        old_labels = labels
        centroids = new_centroids

    wcss = 0
    
    for i in range(len(labels)):
        c_d = centroids[labels[i]]
        p_d = X[i]
        # print(distance_func(p_d, c_d, graph, centroids))
        wcss += distance_func(p_d, c_d, graph, centroids)**2

    return centroids, labels, wcss

                    


def initialize(data, k, graph):
    
    np.random.seed(0)
    data=np.array(data)
    centroids = []
    centroids.append(data[np.random.randint(
            data.shape[0]), :])
    for c_id in range(k - 1):
        dist = []
        for i in range(data.shape[0]):
            point = data[i, :]
            d = sys.maxsize
            for j in range(len(centroids)):
                temp_dist = distance(point, centroids[j],graph,centroids)
                d = min(d, temp_dist)
            dist.append(d)

        dist = np.array(dist)
        next_centroid = data[np.argmax(dist), :]
        centroids.append(next_centroid)
        dist = []
        
    return centroids


if __name__=="__main__":
    file_data=read_file('gml')
    main(file_data)