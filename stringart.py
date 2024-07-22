##############
# String Art #
##############

from PIL import Image, ImageOps, ImageDraw
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def get_imagevector(file):
    
    # Loading image and turn to grayscale
    img = Image.open(file)
    # Getting center of image
    width, height = img.size
    center_x, center_y = width/2, height/2
    
    # Crop the image into a circle with defined radius
    img = img.crop((center_x - 200, center_y - 200, center_x + 200, center_y + 200))
    circle = Image.new(mode="L", size=(400, 400), color = 0)
    circledraw = ImageDraw.Draw(circle)
    circledraw.ellipse((0, 0, 400, 400), fill = 255)
    img.putalpha(circle)
    
    # Get image as a vector of its pixels
    img_vector = np.array(list(zip(*list(img.getdata())))[0])
    img.save("testing.png")
    # Return image vector
    return img_vector

# Plot lines given solved x and number of dimension inputted into 'gen_linematrix'
def plot_lines(x, dim):
    # Initialize the set of starting and end points for the lines given 'dim'
    increment = np.pi/dim
    starts = [increment*i for i in range(1, dim)]
    ends = [increment*i for i in range(1, 2*dim)]
    
    # Get the set of start and end points corresponding to x
    x_tup = []
    for start in starts:
        for end in ends:
            x_tup.append((start, end))
    
    Figure = plt.figure()
    # Set axis and labels
    ax = plt.gca()
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    plt.xticks([])
    plt.yticks([])
    ax.set_aspect('equal')
    ax.axis('off')    
    
    # Plot a circle of size radius centered at (0,0)
    circle = plt.Circle((0,0), 1, fill = False, color = 'black')
    for i in range(len(x_tup)):
        if x[i] == 1:
            l = matplotlib.lines.Line2D([np.cos(x_tup[i][0]), np.cos(x_tup[i][1])],
                                        [np.sin(x_tup[i][0]), np.sin(x_tup[i][1])], 
                                        color = 'black', alpha=0.3)
            ax.add_line(l)
    plt.gca().set_position([0, 0, 1, 1])
    ax.add_artist(circle)
    
#############################
# Generate raster dataframe #
#############################

import io
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Function that outputs the image data for a line going from:
# (cos(start), sin(start)) to (cos(end), sin(end))
def get_linevector(start, end):
    Figure = plt.figure()
    # Set axis and labels
    ax = plt.gca()
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    plt.xticks([])
    plt.yticks([])
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Plot a circle of size radius centered at (0,0)
    l = matplotlib.lines.Line2D([np.cos(start), np.cos(end)], [np.sin(start), np.sin(end)], color = 'black', alpha=0.3)
    ax.add_line(l)
    plt.gca().set_position([0, 0, 1, 1])
    plt.close()
    
    # Convert to PIL image
    buf = io.BytesIO()
    Figure.savefig(buf)
    buf.seek(0)
    img = Image.open(buf).convert('L')
    
    # Getting center of image
    width, height = img.size
    center_x, center_y = width/2, height/2
    # Crop the image into a circle with defined radius
    img = img.crop((center_x - 200, center_y - 200, center_x + 200, center_y + 200))
    circle = Image.new(mode="L", size=(400, 400), color = 0)
    circledraw = ImageDraw.Draw(circle)
    circledraw.ellipse((0, 0, 400, 400), fill = 255)
    img.putalpha(circle)
    
    # Convert into line's raster
    img_vector = list(zip(*list(img.getdata())))[0]
    return img_vector

# Generates matrix columns each corresponding to the image data for a line
def gen_linematrix(dim):
    # Initialize the set of starting and end points for the lines given 'dim'
    increment = np.pi/dim
    starts = [increment*i for i in range(0, dim)]
    ends = [increment*i for i in range(0, 2*dim)]
    # Initialize final matrix
    lin_mat = np.array([0]*160000)
    
    # Loop through all starting and ending points and store values in array
    for start in starts:
        for end in ends:
            line = get_linevector(start, end)
            lin_mat = np.r_['0,2',lin_mat, line]
    # Return resulting matrix
    lin_mat = np.delete(lin_mat, (0), axis=0)
    
    return np.transpose(lin_mat)