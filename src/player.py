from math import sin
import pygame as pg
from src.constants import WIN_WIDTH, WIN_HEIGHT, WIN_CENTER, SCALE


class Player:
    def __init__(self):
        self.right_frames = [pg.transform.scale_by(
            pg.image.load(f"gfx/sub{i}.png").convert_alpha(), SCALE
        ) for i in range(1, 5)]
        self.left_frames = [pg.transform.flip(img, True, False) for img in self.right_frames]
        self.current_frame_list = self.right_frames
        self.current_img = self.right_frames[0]
        self.current_frame = 0

        self.pos = pg.Vector2(WIN_WIDTH / 2 + 50, WIN_HEIGHT / 2)
        self.old_pos = self.pos.copy()
        self.dest = self.pos.copy()
        self.rect = self.current_img.get_frect(center=WIN_CENTER)
        self.vel = pg.Vector2()
        self.speed = 30

        self.angle = 0

    def bob(self, dt: float):
        self.angle += dt * 2
        self.rect.centery = WIN_CENTER[1] + sin(self.angle) * 10

    def animate(self, dt: float):
        self.current_frame += dt * 7
        self.current_frame %= len(self.current_frame_list)
        self.current_img = self.current_frame_list[int(self.current_frame)]

    def update(self, dt: float):
        self.old_pos.xy = self.pos
        self.vel.xy = self.dest - self.pos

        if self.vel:
            self.vel.normalize_ip()
        if not self.pos.distance_to(self.dest) < 1:
            self.pos += self.vel * self.speed * dt
        else:
            self.dest.xy = self.pos

        if self.vel.x < 0:
            self.current_frame_list = self.left_frames
        elif self.vel.x > 0:
            self.current_frame_list = self.right_frames

        self.bob(dt)
        self.animate(dt)

    def draw(self, screen: pg.Surface):
        screen.blit(self.current_img, self.rect)
