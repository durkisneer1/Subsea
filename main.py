from array import array
import pygame as pg
import moderngl as mgl
from src.constants import WIN_SIZE, SCALE
from src.states.gameplay import Gameplay
from src.shaders import vert_shader, frag_shader


pg.init()
pg.mixer.init()

pg.display.set_mode(WIN_SIZE, pg.OPENGL | pg.DOUBLEBUF)
screen = pg.Surface(WIN_SIZE, pg.SRCALPHA)
ctx = mgl.create_context()
pg.display.set_caption("Subsea")
pg.display.set_icon(pg.transform.scale_by(
    pg.image.load("gfx/icon.png"), SCALE
))

clock = pg.time.Clock()
mouse_pos = pg.Vector2()
game = Gameplay()
high_water_color = pg.Color(49, 169, 238)
low_water_color = pg.Color(38, 132, 183)

quad_buffer = ctx.buffer(array("f",[
    # positions, uv coords
    -1.0, 1.0, 0.0, 0.0,  # topleft
    1.0, 1.0, 1.0, 0.0,  # topright
    -1.0, -1.0, 0.0, 1.0,  # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
]))

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])


def surf_to_texture(surf: pg.Surface) -> mgl.Texture:
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (mgl.NEAREST, mgl.NEAREST)
    tex.swizzle = "BGRA"
    tex.write(surf.get_view("1"))
    return tex


def main() -> None:
    music = pg.mixer.Sound("sfx/music.wav")
    music.play(loops=-1)
    music.set_volume(0.4)
    t = 0
    while True:
        dt = clock.tick() / 1000
        t += dt
        mouse_pos.xy = pg.mouse.get_pos()
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                return

        depth = Gameplay.normalize(game.player.pos.y, 0, WIN_SIZE[1])
        screen.fill(high_water_color.lerp(low_water_color, depth))

        game.update(dt, events, mouse_pos)
        game.draw(screen)

        frame_texture = surf_to_texture(screen)
        frame_texture.use(0)
        program["time"] = t
        program["offset"] = game.get_offset().xy
        program["causticStrength"] = (1 - depth) * 5
        render_object.render(mode=mgl.TRIANGLE_STRIP)  # NOQA

        pg.display.flip()
        frame_texture.release()


if __name__ == "__main__":
    main()
