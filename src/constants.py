import noise

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 1280, 720
WIN_CENTER = WIN_WIDTH // 2, WIN_HEIGHT // 2
SCALE = 8
VP_WIDTH, VP_HEIGHT = WIN_WIDTH / SCALE, WIN_HEIGHT / SCALE
VP_HALF_WIDTH, VP_HALF_HEIGHT = int(VP_WIDTH / 2), int(VP_HEIGHT / 2)

GAME_MAP = [
    [
        0 if i == 0 or i == WIN_HEIGHT - 1 or j == 0 or j == WIN_WIDTH - 1 else 1
        for j in range(WIN_WIDTH)
    ]
    for i in range(WIN_HEIGHT)
]

perlin_noise = [[0] * WIN_WIDTH for _ in range(WIN_HEIGHT)]

for y in range(WIN_HEIGHT):
    for x in range(WIN_WIDTH):
        perlin_noise[y][x] = noise.pnoise2(
            x / SCALE / 2,
            y / SCALE / 2,
            octaves=1,
            persistence=0.5,
            repeatx=WIN_WIDTH,
            repeaty=WIN_HEIGHT,
            base=11,
        )

for i in range(1, WIN_HEIGHT - 1):
    for j in range(1, WIN_WIDTH - 1):
        if perlin_noise[i][j] > 0.2:
            GAME_MAP[i][j] = 0
