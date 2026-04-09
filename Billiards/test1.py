import pygame
import math

pygame.init()

# НАСТРОЙКИ
width = 800
height = 450
margin = 30
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
brown = (139, 69, 19)
dark_green = (34, 139, 34)
grey = (50, 50, 50)

FRICTION = 0.985
BALL_RADIUS = 12
POCKET_RADIUS = 22


# КЛАСС ШАРА
class Ball:
    def __init__(self, x, y, color, is_cue=False):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = color
        self.is_cue = is_cue
        self.active = True

    def move(self):
        if not self.active:
            return

        self.x += self.vx
        self.y += self.vy

        self.vx *= FRICTION
        self.vy *= FRICTION

        if abs(self.vx) < 0.05:
            self.vx = 0
        if abs(self.vy) < 0.05:
            self.vy = 0

    def draw(self, surface):
        if not self.active:
            return
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BALL_RADIUS)
        pygame.draw.circle(surface, black, (int(self.x), int(self.y)), BALL_RADIUS, 1)
        if self.color != white:
            pygame.draw.circle(
                surface, (255, 100, 100), (int(self.x - 4), int(self.y - 3)), 4
            )
        else:
            pygame.draw.circle(surface, white, (int(self.x - 4), int(self.y - 3)), 4)


# ИНИЦИАЛИЗАЦИЯ ИГРЫ
def reset_balls():
    bx, by = 550, height // 2
    return [
        Ball(200, height // 2, white, is_cue=True),
        Ball(bx, by, red),
        Ball(bx + 23, by - 13, red),
        Ball(bx + 23, by + 13, red),
        Ball(bx + 46, by, red),
        Ball(bx + 46, by - 26, red),
        Ball(bx + 46, by + 26, red),
    ]


balls = reset_balls()
cue_ball = balls[0]

pockets_pos = [
    (margin, margin),
    (width // 2, margin),
    (width - margin, margin),
    (margin, height - margin),
    (width // 2, height - margin),
    (width - margin, height - margin),
]


def is_line_touching(p1, p2, center, radius):
    if p1 == p2:
        return False

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    mag_sq = dx**2 + dy**2
    u = ((center[0] - p1[0]) * dx + (center[1] - p1[1]) * dy) / mag_sq

    if u < 0:
        closest = p1
    elif u > 1:
        closest = p2
    else:
        closest = (p1[0] + u * dx, p1[1] + u * dy)

    dist = math.hypot(center[0] - closest[0], center[1] - closest[1])
    return dist < radius


# ФУНКЦИИ ОТРИСОВКИ
def draw_table():
    screen.fill(dark_green)

    pygame.draw.rect(screen, brown, (0, 0, width, margin))
    pygame.draw.rect(screen, brown, (0, 0, margin, height))
    pygame.draw.rect(screen, brown, (width - margin, 0, width, height))
    pygame.draw.rect(screen, brown, (0, height - margin, width, height))
    pygame.draw.rect(screen, black, (0, 0, width, height), 2)

    for px, py in pockets_pos:
        pygame.draw.circle(screen, grey, (px, py), POCKET_RADIUS)
        pygame.draw.circle(screen, black, (px, py), POCKET_RADIUS, 2)


# ИГРОВОЙ ЦИКЛ
aiming = False
running = True

while running:
    # 1. ОБРАБОТКА СОБЫТИЙ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if cue_ball.vx == 0 and cue_ball.vy == 0 and cue_ball.active:
                aiming = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if aiming:
                aiming = False
                m_x, m_y = event.pos
                dx = cue_ball.x - m_x
                dy = cue_ball.y - m_y

                power = 0.15
                max_speed = 25
                cue_ball.vx = max(min(dx * power, max_speed), -max_speed)
                cue_ball.vy = max(min(dy * power, max_speed), -max_speed)

    # 2. ФИЗИКА (ДВИЖЕНИЕ)
    for b in balls:
        b.move()

    # 3. ФИЗИКА (СТОЛКНОВЕНИЯ С БОРТАМИ)
    for b in balls:
        if not b.active:
            continue

        if b.x - BALL_RADIUS < margin:
            b.x = margin + BALL_RADIUS
            b.vx *= -0.8
        elif b.x + BALL_RADIUS > width - margin:
            b.x = width - margin - BALL_RADIUS
            b.vx *= -0.8

        if b.y - BALL_RADIUS < margin:
            b.y = margin + BALL_RADIUS
            b.vy *= -0.8
        elif b.y + BALL_RADIUS > height - margin:
            b.y = height - margin - BALL_RADIUS
            b.vy *= -0.8

    # 4. ФИЗИКА (СТОЛКНОВЕНИЯ ШАРОВ)
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            b1, b2 = balls[i], balls[j]
            if not b1.active or not b2.active:
                continue

            dx = b2.x - b1.x
            dy = b2.y - b1.y
            dist = math.hypot(dx, dy)

            if dist < BALL_RADIUS * 2 and dist > 0:
                overlap = (BALL_RADIUS * 2 - dist) / 2
                nx = dx / dist
                ny = dy / dist

                b1.x -= nx * overlap
                b1.y -= ny * overlap
                b2.x += nx * overlap
                b2.y += ny * overlap

                dvx = b1.vx - b2.vx
                dvy = b1.vy - b2.vy

                p = dvx * nx + dvy * ny

                b1.vx -= p * nx * 0.95
                b1.vy -= p * ny * 0.95
                b2.vx += p * nx * 0.95
                b2.vy += p * ny * 0.95

    # 5. ФИЗИКА (ЛУНКИ)
    for b in balls:
        if not b.active:
            continue
        for px, py in pockets_pos:
            if math.hypot(b.x - px, b.y - py) < POCKET_RADIUS:
                if b.is_cue:
                    b.x, b.y = 200, height // 2
                    b.vx, b.vy = 0, 0
                else:
                    b.active = False
                break

    # 6. ОТРИСОВКА
    draw_table()

    if aiming and cue_ball.active:
        m_pos = pygame.mouse.get_pos()
        dx = cue_ball.x - m_pos[0]
        dy = cue_ball.y - m_pos[1]

        target_x = cue_ball.x + dx * 2.5
        target_y = cue_ball.y + dy * 2.5

        p1 = (cue_ball.x, cue_ball.y)
        p2 = (target_x, target_y)

        pygame.draw.line(screen, white, p1, p2, 2)
        pygame.draw.line(screen, grey, p1, m_pos, 1)

        for b in balls:
            if b.active and not b.is_cue:
                if is_line_touching(p1, p2, (b.x, b.y), BALL_RADIUS):
                    pygame.draw.circle(
                        screen, (255, 255, 0), (int(b.x), int(b.y)), BALL_RADIUS + 2, 2
                    )

    for b in balls:
        b.draw(screen)

    # 7. КОНЕЦ ИГРЫ

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
