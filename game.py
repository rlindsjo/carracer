import math
import pygame
import track
from car import Car, ComputerDriver, ManualDriver
from track import Track


class Game:
    def __init__(self):
        self.draw_field = None
        self.draw_look = None
        pygame.init()
        pygame.display.set_caption("Le Williams")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 30
        self.exit = False
        self.track = Track(track.track_1)

        self.font = pygame.font.SysFont('Calibri', 200)

    def run(self):

        race = {
            'started': False,
        }

        red = pygame.image.load("sprites/car_red_small_1.png")
        red = pygame.transform.smoothscale(red, (40.0, 20.0))

        blue = pygame.image.load("sprites/car_blue_small_3.png")
        blue = pygame.transform.smoothscale(blue, (40.0, 20.0))

        green = pygame.image.load("sprites/car_green_small_3.png")
        green = pygame.transform.smoothscale(green, (40.0, 20.0))

        cars = (
            Car(400, 630, length=20, max_velocity=11.0),
            Car(400, 650, length=20, max_acceleration=1.3),
            Car(400, 670, length=20, max_acceleration=1.3)
        )
        car_images = {cars[0]: red, cars[1]: blue, cars[2]: green}

        drivers = (
            ComputerDriver(cars[0], self.track, race, brake_distance=3, coast_distance=8.0),
            ManualDriver(cars[1], race,  keys='wasd'),
            ManualDriver(cars[2], race,  keys='arrows')
        )

        countdown = 30
        while not self.exit:
            dt = self.clock.get_time() / 100
            if not race['started']:
                countdown -= dt
                if countdown < 0:
                    race['started'] = True

            self.__handle_events()

            for driver in drivers:
                driver.look()
                driver.handle(dt)

            for car in cars:
                car.update(dt, self.track)

            # Drawing
            self.__draw_track()
            for car in cars:
                self.__draw_car(car, car_images[car])
            for driver in drivers:
                self.__draw_driver(driver)

            if not race['started']:
                self.__draw_countdown(countdown)

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()

    def __draw_countdown(self, countdown):
        # Draw countdown
        txt = self.font.render(str(math.ceil(countdown / 10)), True, (250, 250, 250))
        pos = ((self.screen.get_width() - txt.get_width()) / 2,
               (self.screen.get_height() - txt.get_height()) / 2)
        self.screen.blit(txt, pos)

    def __handle_events(self):
        # Event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True

    def __draw_car(self, car, car_image):
        rotated = pygame.transform.rotate(car_image, car.angle)
        rect = rotated.get_rect()
        self.screen.blit(rotated, car.position - (rect.width / 2, rect.height / 2))

    def __draw_track(self):
        for x in range(0, 64):
            for y in range(0, 36):
                if self.track.track_tile(x, y):
                    pygame.draw.rect(self.screen, (40, 40, 40), pygame.Rect(x * 20, y * 20, 20, 20))
                else:
                    pygame.draw.rect(self.screen, (20, 100, 40), pygame.Rect(x * 20, y * 20, 20, 20))

    def __draw_driver(self, driver):
        if self.draw_look:
            if isinstance(driver, ComputerDriver):
                pygame.draw.rect(self.screen, (220, 0, 0), pygame.Rect(*driver.look_left, 5, 5))
                pygame.draw.rect(self.screen, (220, 0, 0), pygame.Rect(*driver.look_right, 5, 5))
                pygame.draw.rect(self.screen, (220, 220, 0), pygame.Rect(*driver.look_brake, 5, 5))
                pygame.draw.rect(self.screen, (220, 220, 0), pygame.Rect(*driver.look_coast, 5, 5))


if __name__ == '__main__':
    Game().run()
