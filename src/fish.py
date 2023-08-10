import pygame as pg
from random import choice, randint
from src.constants import WIN_WIDTH, WIN_HEIGHT

class Fish:
    # Fish Colors
    fish_colors = [
        (142, 97, 199, 255),  # Purple
        (95, 135, 199, 255),  # Blue
        (108, 199, 95, 255),  # Green
        (199, 97, 134, 255),  # Red
        (199, 176, 97, 255),  # Yellow
    ]

    def __init__(self, image: pg.Surface):
        self.image = image.copy()
        self.image.fill(choice(self.fish_colors), special_flags=pg.BLEND_RGB_MULT)

        random_height = randint(-WIN_HEIGHT, WIN_HEIGHT * 2)
        direction = choice([True, False])
        self.pos = pg.Vector2(-self.image.get_width() if direction else WIN_WIDTH, random_height)
        self.vel = pg.Vector2(1 if direction else -1, 0)

        if direction:
            self.image = pg.transform.flip(self.image, True, False)

        self.speed = 180

    def update(self, dt: float, offset_vel: pg.Vector2):
        new_vel = self.vel + (-offset_vel.x * 3, -offset_vel.y * 3)
        self.pos += new_vel * self.speed * dt

    def kill(self):
        return self.pos.x > WIN_WIDTH or self.pos.x < -self.image.get_width()

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.pos)
