import pygame as pg
from src.constants import SCALE, WIN_HEIGHT, WIN_SIZE
from src.player import Player
from src.world import World
from src.fish import Fish


class Gameplay:
    def __init__(self):
        self.world = World()
        self.player = Player()
        self.visibility = 0

        self.filter = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.base_light = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.light_color = pg.Color(255, 212, 38, 0)
        self.light_size = pg.Vector2(512)

        for i in range(1, 256):
            circle_surf = pg.Surface(self.light_size, pg.SRCALPHA)
            pg.draw.circle(circle_surf, (1, 1, 1, 1), self.light_size / 2, i)
            self.base_light.blit(circle_surf, (0, 0), special_flags=pg.BLEND_RGBA_ADD)
        self.base_light.fill(self.light_color, special_flags=pg.BLEND_RGBA_MULT)

        self.fish_list = []
        self.fish_base_img = pg.transform.scale_by(
            pg.image.load("gfx/fish.png").convert_alpha(), SCALE
        )
        self.SPAWN_FISH = pg.event.custom_type()
        pg.time.set_timer(self.SPAWN_FISH, 2000)

    def get_offset(self) -> pg.Vector2:
        return self.world.offset

    @staticmethod
    def normalize(value: float, min_value: float, max_value: float) -> float:
        return (value - min_value) / (max_value - min_value)

    def update(self, dt: float, events: list[pg.Event], mouse_pos: pg.Vector2) -> None:
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                goto_pos = mouse_pos / SCALE + self.world.offset
                if not self.world.check_available(goto_pos):
                    return
                self.player.dest = goto_pos
            elif event.type == self.SPAWN_FISH and len(self.fish_list) < 10:
                self.fish_list.append(Fish(self.fish_base_img))

        self.player.update(dt)
        self.world.update(self.player.pos)
        [fish.update(dt, self.player.vel) for fish in self.fish_list]
        self.fish_list = [fish for fish in self.fish_list if not fish.kill()]

        if self.world.check_collision(self.player.pos):
            self.player.pos.xy = self.player.old_pos
            self.player.dest.xy = self.player.pos

        self.visibility = self.normalize(WIN_HEIGHT - self.player.pos.y, 0, WIN_HEIGHT) * 255
        self.filter.fill((self.visibility,) * 3)  # NOQA

    def draw(self, screen: pg.Surface):
        self.world.draw(screen)
        self.player.draw(screen)
        [fish.draw(screen) for fish in self.fish_list]

        light_offset = self.player.rect.center - self.light_size / 2
        self.filter.blit(self.base_light, light_offset, special_flags=pg.BLEND_RGBA_ADD)
        screen.blit(self.filter, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
