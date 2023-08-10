from random import choice
import pygame as pg
from src.constants import (
    GAME_MAP,
    VP_HALF_WIDTH,
    VP_HALF_HEIGHT,
    SCALE,
    WIN_WIDTH,
    WIN_HEIGHT,
)


class World:
    ROCK_COLORS = ["#5c5c5c", "#6c6c6c", "#7c7c7c", "#8c8c8c", "#9c9c9c"]

    def __init__(self):
        self.surf = pg.Surface((SCALE, SCALE))
        self.surf.fill("snow")
        self.offset = pg.Vector2()
        self.viewport_offset = pg.Vector2(VP_HALF_WIDTH, VP_HALF_HEIGHT)

        self.map_dict = {
            (j, i): [GAME_MAP[i][j], choice(self.ROCK_COLORS)]
            for i in range(len(GAME_MAP))
            for j in range(len(GAME_MAP[i]))
        }

        self.render_list = []

    def check_available(self, pos: pg.Vector2) -> bool:
        if not (0 < pos.x < WIN_WIDTH and 0 < pos.y < WIN_HEIGHT):
            return False
        return self.map_dict[(int(pos.x), int(pos.y))][0] == 1

    def check_collision(self, pos: pg.Vector2) -> bool:
        return self.map_dict[(int(pos.x), int(pos.y))][0] == 0

    def update(self, player_pos: pg.Vector2):
        player_x, player_y = int(player_pos.x), int(player_pos.y)

        self.offset.xy = player_pos - self.viewport_offset
        self.render_list = [
            (i, j)
            for i in range(player_x - VP_HALF_WIDTH, player_x + VP_HALF_WIDTH + 1)
            for j in range(player_y - VP_HALF_HEIGHT, player_y + VP_HALF_HEIGHT + 1)
            if -1 < i < WIN_WIDTH and -1 < j < WIN_HEIGHT
        ]

    def draw(self, screen: pg.Surface):
        for pos in self.render_list:
            if self.map_dict[pos][0] == 0:
                pg.draw.rect(
                    screen,
                    self.map_dict[pos][1],
                    (
                        (pos[0] - self.offset.x) * SCALE,
                        (pos[1] - self.offset.y) * SCALE,
                        SCALE,
                        SCALE,
                    ),
                )
