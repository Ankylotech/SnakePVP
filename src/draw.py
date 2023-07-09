import pygame

from snake_types import Vector

global rect_width
global rect_height
player_name_images = {}
font = None
background_color = [0, 0, 30]


def init(players, width, height):
    global font
    global rect_width
    global rect_height

    rect_width = width
    rect_height = height

    font = pygame.font.SysFont("monospace", 20, bold=True)

    for p in players:
        player_name_images[p.name] = font.render(p.name, True, p.color)


def draw(players, obstacles, collectable, screen):
    screen.fill(background_color)
    draw_obstacles(obstacles, screen)
    for player in players:
        draw_snake(player, screen)

    draw_information(players, Vector(10, 10), screen)
    pygame.display.flip()


def draw_snake(player, screen):
    global rect_width
    global rect_height
    for pos in player.snake.positions:
        r = pygame.Rect((pos.x * rect_width, pos.y * rect_height)
                        , (rect_width, rect_height))
        color = player.color
        pygame.draw.rect(screen, color, r)


def draw_obstacles(obstacles, screen):
    global rect_width
    global rect_height
    for obstacle in obstacles:
        x, y = obstacle.x, obstacle.y
        r = pygame.Rect((x * rect_width, y * rect_height)
                        , (rect_width, rect_height))
        color = [255, 0, 0]
        pygame.draw.rect(screen, color, r)


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
