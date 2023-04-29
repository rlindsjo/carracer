from math import copysign, sin, radians, degrees

import pygame
from pygame.math import Vector2


class ManualDriver:
    def __init__(self, car, race, keys='arrows'):
        self.car = car
        self.race = race
        self.penalty = 0.0

        if keys == 'arrows':
            self.right = pygame.K_RIGHT
            self.left = pygame.K_LEFT
            self.accelerate = pygame.K_UP
            self.brake = pygame.K_SPACE
        else:
            # wasd
            self.right = pygame.K_d
            self.left = pygame.K_a
            self.accelerate = pygame.K_w
            self.brake = pygame.K_s

    def look(self):
        # Look at the track yourself
        pass

    def handle(self, dt):

        if self.penalty > 0:
            self.penalty -= dt
            return

        # User input
        pressed = pygame.key.get_pressed()

        if pressed[self.right]:
            self.car.turn_right(dt)
        elif pressed[self.left]:
            self.car.turn_left(dt)
        else:
            self.car.turn_straight(dt)

        if pressed[self.accelerate]:
            if not self.race['started']:
                self.penalty = 10
                return
            self.car.accelerate(dt)
        elif pressed[self.brake]:
            self.car.brake(dt)
        else:
            self.car.coast(dt)


class ComputerDriver:
    def __init__(self, car, track, race, brake_distance=3.0, coast_distance=8.0):
        self.car = car
        self.track = track
        self.race = race

        self.brake_distance = brake_distance
        self.coast_distance = coast_distance

        self.look_brake = self.car.predict(self.brake_distance)
        self.look_coast = self.car.predict(self.coast_distance)
        self.look_left = self.car.predict(4, -20)
        self.look_right = self.car.predict(4, 20)

    def handle(self, dt):
        if not self.race['started']:
            return

        if not self.track.on_track(*self.look_coast) and self.car.velocity.x > 5.0:
            self.car.coast(dt)
        elif not self.track.on_track(*self.look_brake) and self.car.velocity.x > 2.0:
            self.car.brake(dt)
        else:
            self.car.accelerate(dt)

        if not self.track.on_track(*self.look_left):
            self.car.turn_right(dt)
        elif not self.track.on_track(*self.look_right):
            self.car.turn_left(dt)
        else:
            self.car.turn_straight(dt)

    def look(self):
        self.look_brake = self.car.predict(self.brake_distance)
        self.look_coast = self.car.predict(self.coast_distance)
        self.look_left = self.car.predict(4, -20)
        self.look_right = self.car.predict(4, 20)


class Car:
    def __init__(self, x, y, angle=0.0, length=1,
                 max_steering=0.5,
                 max_acceleration=1.0,
                 max_velocity=10.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = max_velocity
        self.brake_deceleration = 5.0
        self.free_deceleration = 0.5

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt, track):
        # In range
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

        if track.on_track(*self.position):
            current_max_velocity = self.max_velocity
        else:
            current_max_velocity = self.max_velocity / 2

        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-current_max_velocity, min(self.velocity.x, current_max_velocity))

        if self.steering:
            turning_radius = self.length / 80.0 / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.angle += degrees(angular_velocity) * dt
        self.position += self.velocity.rotate(-self.angle) * dt

    def crash(self):
        self.velocity = Vector2(0.0, 0.0)

    def predict(self, dist=1.0, offset=0.0):
        return self.position + Vector2(1, 0).rotate(-self.angle + offset) * self.length \
               + self.velocity.rotate(-self.angle + offset) * dist

    def accelerate(self, dt):
        self.acceleration += 1 * dt

    def decelerate(self, dt):
        if self.velocity.x > 0:
            self.acceleration = -self.brake_deceleration * dt

    def brake(self, dt):
        if abs(self.velocity.x) > self.brake_deceleration * dt:
            self.acceleration = -self.brake_deceleration
        else:
            self.acceleration = 0

    def coast(self, dt):
        if abs(self.velocity.x) > dt * self.free_deceleration:
            self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
        elif dt > 0:
            self.acceleration = -self.velocity.x / dt

    def turn_right(self, dt):
        if self.steering < 0:
            self.steering -= 0.1 * dt
        else:
            self.turn_straight(dt)

    def turn_left(self, dt):
        if self.steering > 0:
            self.steering += 0.1 * dt
        else:
            self.turn_straight(dt)

    def turn_straight(self, dt):
        self.steering += -copysign(0.2 * dt, self.steering)
