# Three-Body Simulation

This is a simulation of three bodies interacting gravitationally in a 2-D plane.
Numerical integration of Newton's Law of Gravitation done with the leapfrog algorithm. Animation created with matplotlib's FuncAnimation.

* The input parameters are stored in config.ini, including initial conditions, masses, fudge factors etc.
* The simulation does extend to N-body simulation, alter N_PARTICLES, MASS_MATRIX and the initial condition vectors to add extra particles.
* The output is an mp4 video of the simulation called '3-Body-Simulation.mp4' and a supporting chart named 'Velocity-Analysis.png' for analysis of velocity squared and total velocity over time.

### Run Instructions

To run simulation:
* Make sure you have FFmpeg installed on computer (see link below)
* Open virtual env using `.\three-body-env\Scripts\activate`
* Run using `python .\Three-Body-Simulation.py`
* Run `deactivate` to exit virtual environment

### Notes

* `pip freeze > requirements.txt` for creating requirements file
* `pip install -r /path/to/requirements.txt` for installing requirements to a virtual env
* `virtualenv three-body-env` to create virtual env
* ctl+shift+m opens markdown preview in Atom

### Future Extensions

* Elastic collisions
* Try different animation package

### Links

* FFmpeg installation https://www.wikihow.com/Install-FFmpeg-on-Windows
* Softening https://en.wikipedia.org/wiki/N-body_simulation#Softening
* Leapfrog integration https://en.wikipedia.org/wiki/Leapfrog_integration
* Vector form of Gravity https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation#Vector_form
* More impressive 3-body simulation https://www.youtube.com/watch?v=cev3g826iIQ
* Ideas for other simulations https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/
* Add trail to path https://stackoverflow.com/questions/65194683/i-want-to-have-a-trail-in-the-planet-animation
* Animate multiple plots https://stackoverflow.com/questions/21937976/defining-multiple-plots-to-be-animated-with-a-for-loop-in-matplotlib
* Configparser docs https://docs.python.org/3/library/configparser.html

### Baseline Parameters

There are two 'baseline' videos in the output folder. These are for a simulation reference point in terms of parameter combinations. The baseline parameters themselves are stored in the config folder.
