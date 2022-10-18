import configparser
import json
import math as mt
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# Read input parameters from config file
config = configparser.ConfigParser()
config.read("config/config.ini")

# Set numerical integration constants
TIMESTEP_SIZE = config["Numerical Integration Constants"].getfloat("TIMESTEP_SIZE")
N_PARTICLES = config["Numerical Integration Constants"].getint("N_PARTICLES")
TOTAL_TIME = config["Numerical Integration Constants"].getint("TOTAL_TIME")
MASS_MATRIX = json.loads(config["Numerical Integration Constants"].get("MASS_MATRIX"))
SOFT_PARAM = config["Numerical Integration Constants"].getfloat("SOFT_PARAM")
NUMBER_TIMESTEPS = int(TOTAL_TIME / TIMESTEP_SIZE)
SIMULATION_MATRIX_SHAPE = (NUMBER_TIMESTEPS, N_PARTICLES)
# set initial conditions
POSITION_X0 = json.loads(config["Initial Conditions"].get("POSITION_X0"))
POSITION_Y0 = json.loads(config["Initial Conditions"].get("POSITION_Y0"))
VELOCITY_X0 = json.loads(config["Initial Conditions"].get("VELOCITY_X0"))
VELOCITY_Y0 = json.loads(config["Initial Conditions"].get("VELOCITY_Y0"))
# Set animation constants
TRAIL = config["Animation"].getint("TRAIL")


def force_component(i, j, delta_1, delta_2):
    # Calculate gravitational force along unit vector in direction of delta_1
    return (MASS_MATRIX[i] * MASS_MATRIX[j] * delta_1) / mt.pow(
        (delta_1 * delta_1 + delta_2 * delta_2 + SOFT_PARAM), 1.5
    )


def calculate_force(
    position_matrix_x, position_matrix_y, force_matrix_x, force_matrix_y, timestep_n
):
    # Cycle through all particles to find their total force components
    for i in range(0, N_PARTICLES):
        # Total force components
        force_x_sum = 0.0
        force_y_sum = 0.0
        for j in range(0, N_PARTICLES):
            # Don't compute force of particle on itself!
            if i == j:
                continue
            # Find difference in positions
            delta_x = (
                position_matrix_x[timestep_n][j] - position_matrix_x[timestep_n][i]
            )
            delta_y = (
                position_matrix_y[timestep_n][j] - position_matrix_y[timestep_n][i]
            )
            # Calculate force of particle j on particle i
            force_x = force_component(i, j, delta_x, delta_y)
            force_y = force_component(i, j, delta_y, delta_x)

            force_x_sum += force_x
            force_y_sum += force_y

        force_matrix_x[timestep_n][i] = force_x_sum
        force_matrix_y[timestep_n][i] = force_y_sum


def update_positions(position_matrix, velocity_matrix, force_matrix, timestep_i):
    # Update position matrix for given axis (leapfrog algorithm)
    return position_matrix[timestep_i - 1] + TIMESTEP_SIZE * (
        velocity_matrix[timestep_i - 1]
        + 0.5 * force_matrix[timestep_i - 1] * TIMESTEP_SIZE
    )


def update_velocities(velocity_matrix, force_matrix, timestep_i):
    # Update velocity matrix for given axis (leapfrog algorithm)
    return velocity_matrix[timestep_i - 1] + TIMESTEP_SIZE * 0.5 * (
        force_matrix[timestep_i] + force_matrix[timestep_i - 1]
    )


def simulate():
    # Run numerical integration for particles
    print("Number of timesteps: {:,}".format(NUMBER_TIMESTEPS))

    # Initialise time step matrices
    position_matrix_x = np.zeros(SIMULATION_MATRIX_SHAPE)
    velocity_matrix_x = np.zeros(SIMULATION_MATRIX_SHAPE)
    force_matrix_x = np.zeros(SIMULATION_MATRIX_SHAPE)
    position_matrix_y = np.zeros(SIMULATION_MATRIX_SHAPE)
    velocity_matrix_y = np.zeros(SIMULATION_MATRIX_SHAPE)
    force_matrix_y = np.zeros(SIMULATION_MATRIX_SHAPE)

    # Initial conditions for integration
    position_matrix_x[0] = POSITION_X0
    position_matrix_y[0] = POSITION_Y0
    velocity_matrix_x[0] = VELOCITY_X0
    velocity_matrix_y[0] = VELOCITY_Y0

    # Calculate initial force profile
    calculate_force(
        position_matrix_x, position_matrix_y, force_matrix_x, force_matrix_y, 0
    )

    # Begin simulation!
    for timestep_i in tqdm(range(1, NUMBER_TIMESTEPS)):
        position_matrix_x[timestep_i] = update_positions(
            position_matrix_x, velocity_matrix_x, force_matrix_x, timestep_i
        )
        position_matrix_y[timestep_i] = update_positions(
            position_matrix_y, velocity_matrix_y, force_matrix_y, timestep_i
        )
        calculate_force(
            position_matrix_x,
            position_matrix_y,
            force_matrix_x,
            force_matrix_y,
            timestep_i,
        )
        velocity_matrix_x[timestep_i] = update_velocities(
            velocity_matrix_x, force_matrix_x, timestep_i
        )
        velocity_matrix_y[timestep_i] = update_velocities(
            velocity_matrix_y, force_matrix_y, timestep_i
        )

    # Velocity squared is representative of kinetic energy
    velocity_squared = (
        velocity_matrix_x * velocity_matrix_x + velocity_matrix_y * velocity_matrix_y
    )
    total_velocity_squared = velocity_squared.sum(axis=1)
    # Total velocity is representative of momentum (should be conserved!)
    velocity_sum_x = velocity_matrix_x.sum(axis=1)
    velocity_sum_y = velocity_matrix_y.sum(axis=1)

    # Plot velocity data out vs. time
    fig, ax = plt.subplots(nrows=2, ncols=1)
    ax[0].plot(
        range(0, NUMBER_TIMESTEPS),
        velocity_squared,
        label=[f"Particle {i+1}" for i in range(N_PARTICLES)],
    )
    ax[0].plot(range(0, NUMBER_TIMESTEPS), total_velocity_squared, label="Total")
    ax[0].set_ylabel("Velocity Squared", fontsize=16)
    ax[0].legend()

    ax[1].plot(range(0, NUMBER_TIMESTEPS), velocity_sum_x, label="Sum X")
    ax[1].plot(range(0, NUMBER_TIMESTEPS), velocity_sum_y, label="Sum Y")
    ax[1].set_xlabel("Timestep", fontsize=18)
    ax[1].set_ylabel("Total Velocity", fontsize=16)
    ax[1].legend()

    plt.savefig("output/Velocity-Analysis.png")

    return position_matrix_x, position_matrix_y


def animate(timestep_j, lines, position_matrix_x, position_matrix_y):
    # Update lines with next timestep positions
    for particle, line in enumerate(lines):
        lower_index = max(timestep_j - TRAIL, 0)
        line.set_data(
            position_matrix_x[lower_index:timestep_j, particle],
            position_matrix_y[lower_index:timestep_j, particle],
        )
    return lines
