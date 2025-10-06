
# Importing Packages
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000 # Fixes OverflowError: Exceeded cell block limit


### Define Model ###

G = 58.9639   # AU^3/M yr^2, actual G is 4Pi**2

def ESmodel(state, t):
    """
    Inputs: 
    
    state array: This contains information of Earth's initial position and velocity in the following order: [Earth x-positon, Earth y-position, Earth x-velocity, Earth y-velocity]
    
    t: Time array, contians information about how long the simulation will run and affects the step size of odeint.

    Returns:

    Edstate_dt: The derivatives of Earth's position and velocity. The array is in the same order as state array. [Derivative of Earth x-position, ..., Derivative of Earth y-velocity]
    
    """

    # Define constants
    
    Ex = state[0]
    
    Ey = state[1]
    
    Ex_dot = state[2]
    
    Ey_dot = state[3]
    
    # Equations

    Ex_ddot = -G * Ex / (Ex ** 2 + Ey ** 2) ** (3 / 2)
   
    Ey_ddot = -G * Ey / (Ex ** 2 + Ey ** 2) ** (3 / 2)
  
    Edstate_dt = [Ex_dot, Ey_dot, Ex_ddot, Ey_ddot]
    
    return Edstate_dt

### Earth Initial conditions ###

# Position

EX_0 =  1.01671123 # [AU] Aphelion 1.01671123 = 1(1 + 0.01671123)
EY_0 = 0  # [AU]

# Velocity

EVX_0 = 0.0  # [AU/Yr]
EVY_0 = 7.5545175   # [AU/Yr]

### Jupiter Inital conditions ###

# Position

JX_0 = 0 # [AU]
JY_0 = 4.950429 # [AU] Perihelion

# Velocity

JVX_0 = -3.53437589 # [AU/Yr]
JVY_0 = 0.0  # [AU/Yr]  

### Place intial conditions in a vector ###

EJstate_0 = [EX_0, EY_0, EVX_0, EVY_0, JX_0, JY_0, JVX_0, JVY_0]

### Time Array ###

max_t = 10000

t = np.linspace(0, max_t, 1000000)  # Simulates for a time period of t_max years. 

### Solving ODE ###

# ODE solver function

ESsol = odeint(ESmodel, EJstate_0[0:4], t)


# ES-Earth Solutions

X_ES_Ear = ESsol[:, 0]  # X-coord [AU] of Earth over time interval 
Y_ES_Ear = ESsol[:, 1]  # Y-coord [AU] of Earth over time interval
VX_ES_Ear = ESsol[:, 2] # X-Velocity [AU/yr] of Earth over time interval
VY_ES_Ear = ESsol[:, 3] # Y-Velocity [AU/yr] of Earth over time interval

### Plotting ES Model ###

plt.figure()
plt.plot(X_ES_Ear, Y_ES_Ear, 'blue')
plt.plot(0, 0,'yo', label = 'Sun')      # Yellow marker for Sun's position
plt.plot(X_ES_Ear[0], 0, 'bo', label = 'Earth Initial position') # Blue marker for Earths original position

plt.axis('equal')
plt.xlabel ('X [AU]')
plt.ylabel ('Y [AU]')
plt.title("Earth\'s orbit after {} years".format(max_t))
plt.legend(loc = 'lower right')
plt.show()

### Animation function ###
# To make the animation work in python go to Tools > Preferences > IPython Console > Graphics > Backend and change it from "Inline" to "Automatic"

## ES Animation ##

# Setting up data for animation

trail = 10 # Trail behind the planet

fig, ax = plt.subplots()

s = 81 # speed

# Define animation function

def ES_animator(i, trail=10):

    Earth_ES.set_data(X_ES_Ear[(i - trail) * s:i * s], Y_ES_Ear[(i - trail) * s:i * s])

    ax.set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), xlabel='X [AU]', ylabel='Y [AU]')
    ax.set_title("Earth\'s orbit \n Time: {} yrs \n Speed: {}".format(np.round(t[i * s], decimals = 2), s))

    return Earth_ES,

# Call the function

Earth_ES, = ax.plot([], [], 'o-', markevery= [-1], label = "Earth")
Sun_ES, = ax.plot([0], [0], 'yo', label = "Sun")

ani = animation.FuncAnimation(fig, ES_animator, frames=len(t), fargs=(trail,), interval=10, blit=False)

plt.legend()
plt.show()

# Save animation

#saveani  = animation.FuncAnimation(fig, ES_animator, frames=100, fargs=(trail,), interval=10, blit=False)

#saveani.save("ESmodel-T_{}-S_{}-ANI.gif".format(max_t, s), dpi=300, fps=60)