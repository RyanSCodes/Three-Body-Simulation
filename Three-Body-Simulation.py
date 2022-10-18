"""
N body gravitational simulation code
"""

import matplotlib.animation as animation

from Library import *


def main():
    print("Begin Simulation")
    # Create particle paths
    position_matrix_x, position_matrix_y = simulate()

    # Create figure, axes
    fig = plt.figure()
    ax = plt.axes(
        xlim=(-10, 10),
        ylim=(-10, 10),
        xlabel="x axis",
        ylabel="y axis",
        title="Particle Orbits",
    )
    # Initialise line plot for each particle
    lines = [plt.plot([], [], "o-", markevery=[-1])[0] for i in range(N_PARTICLES)]

    print("Begin Animation")
    # create animation using the animate() function
    myAnimation = animation.FuncAnimation(
        fig,
        animate,
        fargs=(lines, position_matrix_x, position_matrix_y),
        frames=tqdm(range(0, NUMBER_TIMESTEPS)),
        blit=True,
        repeat=True,
    )
    myAnimation.save(
        f"output/{N_PARTICLES}-Body-Simulation.mp4",
        fps=120,
        extra_args=["-vcodec", "libx264"],
    )


if __name__ == "__main__":
    main()
