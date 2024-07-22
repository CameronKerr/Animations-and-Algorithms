########################
# Force-directed graph #
########################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import uniform
from math import sqrt
from matplotlib.animation import FuncAnimation


# Generates edge matrix for a polygon of size 'n'
def gen_edgematrix(n):
    columns = []
    # Generate columns by having each vertex connect to 2 other vertices
    columns.append([0, 1] + [0]*(n-2))
    for i in range(1, n):
        columns.append([0]*(i+1) + [1] + [0]*(n-i-1))
    edge_df = pd.DataFrame(columns).iloc[:, : n]
    edge_df.loc[0, n-1] = 1
    return edge_df
    
# Generates distance matrix for list of points in x, y
def calculate_distance(x, y):
    # Initialize empty distance matrix
    dist_df = pd.DataFrame(np.nan, index = range(len(x)), columns = range(len(x)))
   
    # Loop through upper diagonal of dataframe and fill in distance between respective points
    for i in range(len(x)):
        for j in range(i+1, len(x)):
            distance = sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
            dist_df.loc[i, j] = distance
    return dist_df

# Calculates the forces of attraction produced by springs and repulsion produced by magnets
def calculate_force(vertex, x, y, edge_matrix, dist_matrix):
    # Initialize repulsive and attractive forces vectors
    frep = [(0,0)]
    fattr = [(0,0)]
    
    for v in range(len(x)):
        if v != vertex:
            # Fetch the distance between the points from upper triangle of distance matrix
            distance  = dist_matrix[max(vertex, v)][min(vertex, v)]  
            # Calculate unit vector point from 'vertex' to 'v'            
            unit_vector = ((x[v] - x[vertex])/distance, (y[v] - y[vertex])/distance)
            
            # Calculate repulsive and attractive forces depending on if their is an edge between the vertices
            edge = edge_matrix.loc[min(vertex, v), max(vertex, v)]
            if edge == 0:
                frep.append((2/distance**2*(-1)*unit_vector[0], 2/distance**2*(-1)*unit_vector[1]))
            elif edge == 1:
                fattr.append((np.log(distance)*unit_vector[0], np.log(distance)*unit_vector[1]))
    displacement_vector = (sum(list(zip(*(frep + fattr)))[0]), (sum(list(zip(*(frep + fattr)))[1])))
    return displacement_vector 
    
# Follow the Eades algorithm to recursively move the points based on the displacement vector
def eades_algorithm(edge_matrix, num_iterations, factor, original_x, original_y):  
    
    # Initialize points 
    x = original_x
    y = original_y
    
    # Optimize graph through num_iterations
    t = 0
    while t < num_iterations:
        # Get distance matrix for current iteration
        dist_matrix = calculate_distance(x, y)
        if len(dist_matrix.round(3).stack().unique()) == 1:
            break
        # Initialize list for new x, y values
        new_x = []
        new_y = []        
        for i in range(len(x)):
            # Calculate new x, y values through displacement vector
            displacement = calculate_force(i, x, y, edge_matrix, dist_matrix)
            new_x.append(x[i] + factor*displacement[0])
            new_y.append(y[i] + factor*displacement[1])
        # Update x and y
        x = new_x
        y = new_y
        
        t = t + 1
    return (x, y)
    
# Animation function plots a specific iteration
def animation_function(iteration):
    # Get points at that iteration
    points = eades_algorithm(edge_matrix, iteration, 0.8, original_x, original_y)
    x = points[0]
    y = points[1]
    
    # Plot points
    plt.cla()
    for i in range(0, (len(x)-1)):
        plt.plot(x[i:i+2], y[i:i+2], 'ro-')
    plt.plot([x[0], x[len(x)-1]], [y[0], y[len(y)-1]], 'ro-')
    plt.axis('off')
    
if __name__ == '__main__':
    
    # Prompt user for size of n-gon to generate
    n = int(input("Enter the n-gon you want to generate:"))
    
    edge_matrix = gen_edgematrix(n)
    
    # Generate random points
    original_x, original_y = [], []
    [original_x.append(uniform(0, 1)) for i in range(n)]
    [original_y.append(uniform(0, 1)) for i in range(n)]   
    
    # Create and save animation
    Figure = plt.figure()
    anim_created = FuncAnimation(Figure, animation_function, 
                                 frames = 500, interval=100)
    anim_created.save(filename='force-directedpolygon.mp4')
    plt.close()      