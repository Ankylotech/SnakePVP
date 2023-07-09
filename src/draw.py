import pygame

from snake_types import Vector

global sq_size
player_name_images = {}
font = None
background_color = [0, 0, 30]


def init(players, size):
    global font
    global sq_size

    sq_size = size

    font = pygame.font.SysFont("monospace", 20, bold=True)

    for p in players:
        player_name_images[p.name] = font.render(p.name, True, p.color)


def draw(players, obstacles, collectable, screen):
    screen.fill(background_color)
    draw_obstacles(obstacles, screen)
    for player in players:
        draw_snake(player, screen)

    draw_collectables(collectable,screen)

    draw_information(players, Vector(10, 10), screen)
    pygame.display.flip()


def draw_snake(player, screen):
    global sq_size
    for pos in player.snake.positions:
        r = pygame.Rect((pos.x * sq_size, pos.y * sq_size)
                        , (sq_size, sq_size))
        color = player.color
        pygame.draw.rect(screen, color, r)


def draw_obstacles(obstacles, screen):
    global sq_size
    for obstacle in obstacles:
        x, y = obstacle.x, obstacle.y
        r = pygame.Rect((x * sq_size, y * sq_size)
                        , (sq_size, sq_size))
        color = [255, 0, 0]
        pygame.draw.rect(screen, color, r)


def draw_collectables(collectables, screen):
    global sq_size
    for collectable in collectables:
        pygame.draw.circle(screen, collectable.color, (collectable.position.x * sq_size + sq_size / 2, collectable.position.y * sq_size + sq_size / 2), sq_size/2)


def draw_text(text, color, pos, screen, center=True):
    global font
    (dx, dy) = font.size(text)
    adj_pos = pos - Vector(dx, dy) / 2 if center else pos
    screen.blit(font.render(text, False, color)
                , tuple(adj_pos))


def draw_information(players, pos, screen):
    global font

    dx = Vector(40, 0)
    dy = Vector(0, 30)
    pos += dy
    for p in players:
        draw_text(str(p.score), p.color, pos, screen, center=False)
        screen.blit(player_name_images[p.name], tuple(pos + dx))
        pos += dy
