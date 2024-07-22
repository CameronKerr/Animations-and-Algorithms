#####################################
# Drawing pictures with probability #
#####################################

from PIL import Image, ImageOps
from numpy import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial import distance

# Function which performs a single bernoulli trial 
def bernoulli_trial(p):
    return random.random() < p

# Function for getting points to draw given file
def generate_points(file):
    # Loading image and converting to grayscale
    img = Image.open(file)
    
    gray_img = ImageOps.grayscale(img)
    # Get width and height of image in pixels
    width, height = gray_img.size
    # Initialize point lists
    X, Y = [], []
    
    # Loop through pixels
    for i in range(width):
        for j in range(height):
            # Calculate grayscale value and related probability value
            gr = gray_img.getpixel((i, j))
            prob = (1 - gr/255)*0.1
            # Add the point if it passes the bernoulli trial
            if bernoulli_trial(prob):
                X.append(i)
                Y.append(j)
    return X, Y

# Animation function for the certain frame
def animation_function(frame):
    if distance.euclidean((X[frame], Y[frame]), (X[frame+2], Y[frame+2])) < 100:   
        plt.plot(X[frame:frame+2], Y[frame:frame+2], 'ro-', linewidth=0.5, markersize=0.5)
        

# Get path from points X, Y
def get_path(X, Y):
    # Initialize the unresolved points and the path
    unresolved = list(zip(X[1:], Y[1:]))
    path = [(X[0], Y[0])]
    while unresolved != []:
        # Calculate how far away the most recent addition of the path is to all unresolved points
        distances = [distance.euclidean(i, path[-1]) for i in unresolved]
        # Get the point closest to the most recent addition
        mindistance = distances.index(min(distances))
        # Add the point to the path and remove it from the unresolved points
        path.append(unresolved[mindistance])
        unresolved.remove(unresolved[mindistance])
    X = list(zip(*path))[0]
    Y = list(zip(*path))[1]
    return X, Y
    
    
if __name__ == '__main__':
    filename = input("Enter filename:")
    
    # Generate initial plot
    img = Image.open(filename)
    width, height = img.size
    Figure = plt.figure()
    # Set axis
    ax = plt.gca()
    ax.set_xlim([0, width])
    ax.set_ylim([0, height])
    
    # Get points for file
    X, Y = generate_points(filename)
    X, Y = get_path(X, Y)
    
    plt.axis('equal')
    
    #Create and save animation
    anim_created = FuncAnimation(Figure, animation_function,
                                 frames = len(X), interval = 10)
    anim_created.save(filename = 'prob_drawing.mp4')
    plt.close() 