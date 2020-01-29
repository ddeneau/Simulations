# Simulation of two dimensional orbital mechanics.

import numpy
import scipy.constants
import pygame
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

    def __init__(self, semi_major, semi_minor, focus, eccentricity):
        self.semi_major = semi_major   # The semi-major axis
        self.semi_minor = semi_minor  # The semi-minor axis
        self.focus = focus  # Focus of ellipse
        self.eccentricity = eccentricity
        self.theta = 0.01  # Angle between radius and x-axis
        self.phi = 0.01  # Angle between radius, from focus, and x-axis
        self.star = Body(100, 45, int(WIDTH / 2), int(HEIGHT / 2))  # main star (mass, radius)
        self.planet = Body(1, 2, int(WIDTH / 2) + self.semi_major, int(HEIGHT / 2))    # First planet (mass, radius)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Making of the screen

    # Updates alpha with new angular acceleration.
    def compute_force(self):
        mass = self.star.mass
        r_squared = numpy.power(self.planet.distance, 2)

        self.planet.alpha = scipy.constants.gravitational_constant * mass / r_squared

    # Calculates new angular velocity
    def compute_angular_velocity(self):
        self.planet.omega = numpy.sqrt(self.planet.alpha / (self.planet.mass * numpy.power(self.semi_major, 3)))

    # Update x and y values of planet based off of Kepler's Law's
    def compute_radial_vector(self):
        x = (self.semi_major * numpy.cos(self.theta)) - self.eccentricity
        y = (self.semi_major * numpy.sin(self.theta) * (1 - numpy.power(self.eccentricity, 2)))

        self.planet.update_state(x, y, self.theta, self.planet.omega)

    # Keeps us between 0 and 2Pi
    def check_angle(self):
        if self.phi > 2 * numpy.pi:
            self.phi = 0
        if self.theta > 2 * numpy.pi:
            self.theta = 0

    # Updates value of angle between semi-major axis and the vector from the star to the planet.
    def update_angle(self):
        self.theta += numpy.arctan(numpy.tan(self.phi / 2) /
                                   numpy.sqrt((1 + self.eccentricity)/(1 - self.eccentricity)))

    # Computations of tick of the simulation.
    def run_sim_frame(self):
        self.screen.fill((100, 100, 100))
        self.check_angle()  # Make sure no angle exceeds 2pi rads
        self.compute_force()  # Force and angular acceleration equation
        self.compute_angular_velocity()  # Angular velocity equation.
        self.compute_radial_vector()  # Updates x and y positions.
        self.update_angle()  # Increments angle to move time forward.

    # Coordinate adjustment to fit with pygame coordinate scheme.

    # Initializes simulation as well as pygame window.
    def init_graphics(self):
        clock = pygame.time.Clock()
        pygame.display.set_caption('Orbit Simulation')  # Name for the window
        self.screen.fill((100, 100, 100))  # This syntax fills the background colour
        pygame.display.flip()
        r_star = self.star.radius
        r_planet = self.planet.radius
        running = True
        while running:
            for event in pygame.event.get():
                if event.type is pygame.KEYDOWN:
                    if event.key is pygame.K_d:
                        self.theta += 0.2
                        self.phi += 0.2
                    elif event.key is pygame.K_a:
                        self.theta -= 0.2
                        self.theta -= 0.2

                if event.type == pygame.QUIT:
                    running = False

            self.run_sim_frame()
            adjust_coordinates(self.planet)
            pygame.draw.circle(self.screen, (200, 0, 0), (self.star.x, self.star.y), r_star, r_star)
            pygame.draw.circle(self.screen, (0, 200, 0), (self.planet.x, self.planet.y), r_planet, r_planet)
            pygame.display.update()
            clock.tick(100)

        pygame.quit()


# A object that experience state changes in relation to physical forces.
class Body:

    def __init__(self, mass, radius, x, y):
        self.mass = mass  # Mass of body.
        self.radius = radius  # Radius of body
        self.distance = 500  # Starting distance from star on x-axis, Starting at 0 radians.
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.omega = 0  # Angular velocity
        self.alpha = 0  # Angular acceleration

    # Change state of body based on parameters.
    def update_state(self, x, y, alpha, omega):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.omega = omega
        print(x, y)


# Runs program.
m = Mechanics(400, 200, 175, 0.5)
m.init_graphics()