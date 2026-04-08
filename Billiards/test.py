import pygame
import math

pygame.init()

width = 800
height = 450
margin = 30
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
brown = (139, 69, 19)
green = (30, 255, 30)
dark_green = (34, 139, 34)
grey = (90, 90, 90)

x, y = 200, height // 2
bx, by = 530, height // 2
speed_x = 0
speed_y = 0
speed_bx = 0
speed_by = 0
friction = 0.98
aiming = False
red_balls = [
    [bx, by, 0, 0],
    [bx + 23, by - 13, 0, 0],
    [bx + 23, by + 13, 0, 0],
    [bx + 46, by, 0, 0],
    [bx + 46, by - 26, 0, 0],
    [bx + 46, by + 26, 0, 0],
]


def ball(color, x, y):
    pygame.draw.circle(screen, color, (x, y), 12)
    pygame.draw.circle(screen, black, (x, y), 12, 1)
    pygame.draw.circle(screen, white, (x - 4, y - 3), 4)


def table():  # Очистка
    pygame.draw.rect(screen, brown, (0, 0, width, margin))
    pygame.draw.rect(screen, brown, (0, 0, margin, height))
    pygame.draw.rect(screen, brown, (width - margin, 0, width, height))
    pygame.draw.rect(screen, brown, (0, height - margin, width, height))
    pygame.draw.rect(screen, black, (0, 0, width, height), 1)
    pygame.draw.rect(
        screen, black, (margin, margin, width - margin * 2, height - margin * 2), 1
    )


def pockets():
    pygame.draw.circle(screen, grey, (margin, margin), 22)
    pygame.draw.circle(screen, black, (margin, margin), 22, 1)
    pygame.draw.circle(screen, grey, (width // 2, margin), 20)
    pygame.draw.circle(screen, black, (width // 2, margin), 20, 1)
    pygame.draw.circle(screen, grey, (width - margin, margin), 22)
    pygame.draw.circle(screen, black, (width - margin, margin), 22, 1)

    pygame.draw.circle(screen, grey, (margin, height - margin), 22)
    pygame.draw.circle(screen, black, (margin, height - margin), 22, 1)
    pygame.draw.circle(screen, grey, (width // 2, height - margin), 20)
    pygame.draw.circle(screen, black, (width // 2, height - margin), 20, 1)
    pygame.draw.circle(screen, grey, (width - margin, height - margin), 22)
    pygame.draw.circle(screen, black, (width - margin, height - margin), 22, 1)


running = True
while running:
    keys = pygame.key.get_pressed()

    # 1. Обработка выхода
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and speed_x == 0 and speed_y == 0:
            if event.button == 1:
                aiming = True
                power = 0.1

        if event.type == pygame.MOUSEBUTTONUP and speed_x == 0 and speed_y == 0:
            if event.button == 1:
                aiming = False
                m_x, m_y = event.pos
                dx = x - m_x
                dy = y - m_y

                speed_x = dx * power
                speed_y = dy * power

    # 2. Управление

    x -= speed_x
    y -= speed_y
    speed_x *= friction
    speed_y *= friction

    if abs(speed_x) < 0.1:
        speed_x = 0
    if abs(speed_y) < 0.1:
        speed_y = 0

    for b_red in red_balls:
        b_red[0] -= b_red[2]
        b_red[1] -= b_red[3]
        b_red[2] *= friction
        b_red[3] *= friction

        if abs(b_red[2]) < 0.1:
            b_red[2] = 0
        if abs(b_red[3]) < 0.1:
            b_red[3] = 0

    # 3. Столкновения
    if x - 12 < margin or x + 12 > width - margin:
        speed_x *= -1
    if y - 12 < margin or y + 12 > height - margin:
        speed_y *= -1

    for b_red in red_balls:
        if b_red[0] - 12 < margin:
            b_red[0] = margin + 12
            b_red[2] *= -0.8
        elif b_red[0] + 12 > width - margin:
            b_red[0] = width - margin - 12
            b_red[2] *= -0.8

        if b_red[1] - 12 < margin:
            b_red[1] = margin + 12
            b_red[3] *= -0.8
        elif b_red[1] + 12 > height - margin:
            b_red[1] = height - margin - 12
            b_red[3] *= -0.8

    for b_red in red_balls:
        dx = b_red[0] - x
        dy = b_red[1] - y
        distance = math.hypot(dx, dy)  # Расстояние между центрами

        if distance < 24:  # Столкновение произошло
            # 1. РЕШАЕМ ПРОБЛЕМУ СЛИПАНИЯ (Раздвигаем шары)
            overlap = 24 - distance
            # Находим направление (единичный вектор)
            nx = dx / distance
            ny = dy / distance

            # Раздвигаем их, чтобы не было "залипания"
            x -= nx * (overlap / 2)
            y -= ny * (overlap / 2)
            b_red[0] += nx * (overlap / 2)
            b_red[1] += ny * (overlap / 2)

            # 2. РЕШАЕМ ПРОБЛЕМУ НАПРАВЛЕНИЯ (Упругий удар)
            # Проекция скорости на нормаль (линию удара)
            # v1n - скорость битка вдоль линии удара
            # v2n - скорость красного вдоль линии удара
            v1n = speed_x * nx + speed_y * ny
            v2n = b_red[2] * nx + b_red[3] * ny

            # Обмен скоростями вдоль нормали (упрощенно для равных масс)
            # Биток отдает свою энергию, красный забирает
            impulse = v1n - v2n

            speed_x -= impulse * nx
            speed_y -= impulse * ny
            b_red[2] += impulse * nx
            b_red[3] += impulse * ny

            # Добавим небольшую потерю энергии при ударе (0.9)
            speed_x *= 0.9
            speed_y *= 0.9
            b_red[2] *= 0.9
            b_red[3] *= 0.9

    # 4. Отрисовка
    screen.fill(green)
    table()
    pockets()
    ball(white, x, y)
    for b_red in red_balls:
        ball(red, b_red[0], b_red[1])
    if aiming:
        pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, white, (x, y), pos, 1)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
