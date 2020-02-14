# Simulation of two dimensional orbital mechanics.

import numpy
import scipy.constants
import pygame
import random
WIDTH = 1200
HEIGHT = 800


# Simulation state changes.
def adjust_coordinates(body):
    if body.x < 0:
        body.x += 500
    else:
        body.x += 500
    if body.y < 0:
        body.y += 500
    else:
        body.y += 500

    body.x = (int(body.x))
    body.y = (int(body.y))


class Mechanics:

    def __init__(self, semi_major, semi_minor, focus):
        self.semi_major = semi_major   # The semi-major axis
        self.semi_minor = semi_minor  # The semi-minor axis
        self.focus = focus  # Focus of ellipse
        self.star = Body(50, 25, int(WIDTH / 2), int(HEIGHT / 2), 0, 0, 0)  # main star (mass, radius)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Making of the screen
        self.bodies = list()
        self.generate_bodies()

    def generate_bodies(self):
        for i in range(3):
            mass = random.randint(1, 5)
            radius = mass
            x = int(WIDTH / random.randint(1, 5))
            y = int(HEIGHT / random.randint(1, 5))
            e = random.randint(1, 1000) / 1000
            m = i / 100
            self.bodies.append(Body(mass, radius, x, y, e, e + m, e + m))

    # Updates alpha with new angular acceleration.
    def compute_force(self, body):
        mass = self.star.mass
        r_squared = numpy.power(body.distance, 2)

        body.alpha = scipy.constants.gravitational_constant * mass / r_squared

    # Calculates new angular velocity
    def compute_angular_velocity(self, body):
        body.omega = numpy.sqrt(body.alpha / (body.mass * numpy.power(self.semi_major, 3)))

    # Update x and y values of planet based off of Kepler's Law's
    def compute_radial_vector(self, body):
        x = (self.semi_major * numpy.cos(body.theta)) - body.eccentricity
        y = (self.semi_major * numpy.sin(body.theta) * (1 - numpy.power(body.eccentricity, 2)))

        body.update_state(x, y, body.theta, body.omega)

    # Computations of tick of the simulation.
    def run_sim_frame(self):
        for body in self.bodies:
            self.screen.fill((100, 100, 100))
            body.check_angle()  # Make sure no angle exceeds 2pi rads
            self.compute_force(body)  # Force and angular acceleration equation
            self.compute_angular_velocity(body)  # Angular velocity equation.
            self.compute_radial_vector(body)  # Updates x and y positions.
            body.update_angle()  # Increments angle to move time forward.

    # Coordinate adjustment to fit with pygame coordinate scheme.

    # Initializes simulation as well as pygame window.
    def init_graphics(self):
        clock = pygame.time.Clock()
        pygame.display.set_caption('Orbit Simulation')  # Name for the window
        self.screen.fill((100, 100, 100))  # This syntax fills the background colour
        pygame.display.flip()

        r_planets = list()
        r_star = self.star.radius

        for body in self.bodies:
            r_planets.append(body.radius)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.run_sim_frame()

            for body in self.bodies:
                adjust_coordinates(body)

            pygame.draw.circle(self.screen, (200, 0, 0), (self.star.x, self.star.y), r_star, r_star)

            for body in self.bodies:
                pygame.draw.circle(self.screen, (0, 200, 0), (body.x, body.y), body.radius, body.radius)

            pygame.display.update()
            clock.tick(100)

        pygame.quit()


# A object that experience state changes in relation to physical forces.
class Body:

    def __init__(self, mass, radius, x, y, eccentricity, theta, phi):
        self.mass = mass  # Mass of body.
        self.radius = radius  # Radius of body
        self.distance = numpy.sqrt(x**2 + y**2) # Starting distance from star on x-axis, Starting at 0 radians.
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.omega = 0  # Angular velocity
        self.alpha = 0  # Angular acceleration
        self.theta = theta  # Angle between radius and x-axis
        self.phi = phi  # Angle between radius, from focus, and x-axis
        self.eccentricity = eccentricity

    # Change state of body based on parameters.
    def update_state(self, x, y, alpha, omega):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.omega = omega
        print(x, y, self.eccentricity)

    # Keeps us between 0 and 2Pi
    def check_angle(self):
        if self.phi > 2 * numpy.pi:
            self.phi = 0
        if self.theta > 2 * numpy.pi:
            self.theta = 0

    # Updates value of angle between semi-major axis and the vector from the star to the planet.
    def update_angle(self):
        self.theta += numpy.arctan(numpy.tan(self.phi / 2) /
                                   numpy.sqrt((1 + self.eccentricity) / (1 - self.eccentricity)))


# Runs program.
m = Mechanics(200, 150, 100)
m.init_graphics()
