##################
# Mandelbrot Set #
##################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Add complex numbers a and b
def add_complex(a, b):
    return (a[0] + b[0], a[1] + b[1])
# Multiply complex numbers a and b
def mult_complex(a, b):
    return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])
# Calculate magnitude of complex number
def magnitude_complex(a):
    return np.sqrt(a[0]**2 + a[1]**2)

# Get iterations
def iteration(c, max_iteration):
    # Initialize z
    z = (0, 0)
    
    for iteration in range(1, max_iteration+1):
        # Calculate next iteration
        z = add_complex(mult_complex(z, z) , c)
        
        # Break if z's magnitude is greater than 4 since the sequence must be unbounded
        if magnitude_complex(z) > 4:
            break
    return iteration
 
def animation_function(frame):
    # Create real and imaginary axis centered on a and b based on frame
    rl_axis = np.linspace(a - frame*0.1, a + frame*0.1, 1000)
    im_axis = np.linspace(b - frame*0.1, b + frame*0.1, 1000)
    
    # Initialize empty set of mandelbrot set
    mandelbrot = np.empty((1000, 1000))
    # Loop over all points and fill that entry of mandelbrot with the number of iterations
    for i in range(0, 1000):
        for j in range(0, 1000):
            c = (rl_axis[i],im_axis[j])
            mandelbrot[i, j] = iteration(c, 1000)
    # Plot mandelbrot set for this frame
    plt.imshow(mandelbrot.T, interpolation = "nearest")
    plt.show()    
    
if __name__ == '__main__':
    
    # Prompt user for point to zoom in on
    a = float(input("Enter real part of center point:"))
    b = float(input("Enter imaginary part of center point:"))
    
    # Create and save animation
    Figure = plt.figure()
    anim_created = FuncAnimation(Figure, animation_function, 
                                 frames = 1, interval=250)
    anim_created.save(filename='Mandelbrot.mp4')
    plt.close()    
