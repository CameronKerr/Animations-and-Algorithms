#######################
# Sierpinski Triangle #
#######################

from numpy import sqrt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Given a line from x to y get the 3 line segments connecting x to y which 
# follow the hexagon which is bisected by the line from x to y. 
def split_line(x, y, direction):
    d = (y[0] - x[0], y[1] - x[1])
    if direction == 'up':
        # p and q are the vertices of the upper half of the hexagon
        p = (x[0] + d[0]/4 - sqrt(3)*d[1]/4, x[1] + d[1]/4 + sqrt(3)*d[0]/4)
        q = (x[0] + 3*d[0]/4 - sqrt(3)*d[1]/4, x[1] + 3*d[1]/4 + sqrt(3)*d[0]/4)
    elif direction == 'down':
        # p and q are the vertices of the bottom half of the hexagon
        p = (x[0] + d[0]/4 + sqrt(3)*d[1]/4, x[1] + d[1]/4 - sqrt(3)*d[0]/4)
        q = (x[0] + 3*d[0]/4 + sqrt(3)*d[1]/4, x[1] + 3*d[1]/4 - sqrt(3)*d[0]/4)  
    else:
        return "Invalid direction, input 'up' or 'down'"
    return [x, p, q]

# Get list of points for sierpinski arrowhead construction from 1 to max_iteration   
def sierpinski_iterations(max_iteration):
    # Initialize list of points in each iteration (list of lists)
    meta_list = []
    
    # Initialize initial list of points
    sierpinski = split_line((0,0), (4,0), 'up')
    sierpinski.append((4,0))
    meta_list.append(sierpinski)
    
    # Fill in meta list with the points of the Sierpinski triangle at each iteration
    iteration = 0
    while iteration < max_iteration:
        new_sierpinski = []
        # Loop through all points and create new points for next iteration 
        # based on the arrowhead construction of the Sierpinski gasket
        for i in range(0, (len(sierpinski)-1)):
            if i % 2 == 0:
                if len(meta_list) % 2 == 0:
                    direc = 'up'
                else:
                    direc = 'down'
            else:
                if len(meta_list) % 2 == 0:
                    direc = 'down'
                else: 
                    direc = 'up'
                   
            newpoints = split_line(sierpinski[i], sierpinski[i + 1], direc)
            new_sierpinski.append(newpoints[0])
            new_sierpinski.append(newpoints[1])
            new_sierpinski.append(newpoints[2])
        # Append the new sierpinski list of points to the meta list
        new_sierpinski.append(sierpinski[-1])
        sierpinski = new_sierpinski
        meta_list.append(sierpinski)
        iteration += 1
    return meta_list

# Animation function plots the given sierpinski triangle for that frame
def animation_function(frame):
    plt.cla()
    sierpinski = meta_list[frame-1]
    x = list(zip(*sierpinski))[0]
    y = list(zip(*sierpinski))[1]
    for i in range(0, (len(sierpinski)-1)):
        plt.plot(x[i:i+2], y[i:i+2], 'ro-')
    
if __name__ == '__main__':
    
    # Prompt user for point to zoom in on
    max_triangle = int(input("Enter max triangle to visualize:"))
    
    # Create and save animation
    Figure = plt.figure()
    meta_list = sierpinski_iterations(max_triangle)
    anim_created = FuncAnimation(Figure, animation_function, 
                                 frames = max_triangle, interval=500)
    anim_created.save(filename='Sierpinski.mp4')
    plt.close()  
    

    
        