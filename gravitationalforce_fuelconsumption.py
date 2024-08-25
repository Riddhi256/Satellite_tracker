import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
m1 = 5.972e24    # Mass of Earth (kg)
m2 = 1000        # Mass of spacecraft (kg)
fuel_mass = 500  # Initial fuel mass (kg)
fuel_consumption_rate = 0.1  # Fuel consumption rate (kg/s)
thrust = 1e3     # Thrust provided by the spacecraft (N)

# Initial conditions
r1 = np.array([0, 0])  # Earth at origin
r2 = np.array([7000e3, 0])  # Spacecraft 7000 km from Earth
v1 = np.array([0, 0])  # Earth stationary
v2 = np.array([0, 7.8e3])  # Spacecraft initial velocity (m/s)

# Initial state vector
y0 = np.concatenate((r1, r2, v1, v2, [fuel_mass]))

def equations(t, y):
    r1, r2, v1, v2, fuel_mass = y[:2], y[2:4], y[4:6], y[6:8], y[8]
    r12 = np.linalg.norm(r2 - r1)
    a1 = G * m2 * (r2 - r1) / r12**3
    a2 = G * m1 * (r1 - r2) / r12**3

    # Fuel consumption and thrust
    if fuel_mass > 0:
        fuel_mass -= fuel_consumption_rate * t
        thrust_acceleration = thrust / m2
        a2 += thrust_acceleration * (r2 - r1) / r12

    return np.concatenate((v1, v2, a1, a2, [-fuel_consumption_rate]))

# Time span for the simulation (in seconds)
t_span = (0, 3600)  # 1 hour

# Solve the differential equations
sol = solve_ivp(equations, t_span, y0, method='RK45', rtol=1e-9)

# Extract positions
r1_sol = sol.y[:2]
r2_sol = sol.y[2:4]

# Plot the results
plt.plot(r1_sol[0], r1_sol[1], label='Earth')
plt.plot(r2_sol[0], r2_sol[1], label='Spacecraft')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.legend()
plt.title('Gravitational Force and Fuel Consumption Simulation')
plt.show()