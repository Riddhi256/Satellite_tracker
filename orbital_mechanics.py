import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Gravitational constant (km^3/s^2)
mu = 398600

# Define the equations of motion in 2D
def equations_of_motion(t, y):
    r = np.sqrt(y[0]**2 + y[1]**2)
    ax = -mu * y[0] / r**3
    ay = -mu * y[1] / r**3
    return [y[2], y[3], ax, ay]

# Initial conditions: [x0, y0, vx0, vy0]
initial_conditions = [7000, 0, 0, 7.5]

# Time span (seconds)
t_span = (0, 3600)  # 1 hour

# Solve the differential equations
solution = solve_ivp(equations_of_motion, t_span, initial_conditions, method='RK45', rtol=1e-8)

# Extract the results
x, y = solution.y[0], solution.y[1]

# Plot the orbit
plt.figure()
plt.plot(x, y)
plt.xlabel('X (km)')
plt.ylabel('Y (km)')
plt.title(' Orbital  Mechanics Simulation')
plt.grid(True)
plt.axis('equal')
plt.show()
