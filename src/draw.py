import copy

import pygame

from snake_types import Vector

global sq_size
global orange_portal
global blue_portal
global portal_num
player_name_images = {}
font = None
background_color = [0, 0, 30]
green = pygame.Color(0, 255, 0)


def replace(image, color1, color2):
    w, h = image.get_size()
    result = copy.copy(image)
    for x in range(w):
        for y in range(h):
            c = image.get_at((x, y))
            if color1 == c:
                result.set_at((x, y), color2)
            else:
                result.set_at((x, y), pygame.Color(0, 0, 0, 0))
    return result


def init(players, size):
    global font
    global sq_size
    global orange_portal
    global blue_portal
    global portal_num

    portal_num = 0
    sq_size = size
    portal = pygame.transform.scale(pygame.image.load('../images/portal.png'), (size, size))
    orange = pygame.Color(255, 127, 0)
    blue = pygame.Color(0, 20, 255)
    orange_portal = replace(portal, green, orange)
    blue_portal = replace(portal, green, blue)
    font = pygame.font.SysFont("monospace", 20, bold=True)

    for p in players:
        player_name_images[p.name] = font.render(p.name, True, p.color)


def draw(players, obstacles, bonuses, portals, screen, remainingSteps):
    screen.fill(background_color)
    draw_obstacles(obstacles, screen)
    for player in players:
        draw_snake(player, screen)

    draw_bonuses(bonuses, screen)

    for portal in portals:
        draw_portal(portal, screen)

    draw_information(players, Vector(10, 10), screen, remainingSteps)
    pygame.display.flip()


def draw_snake(player, screen):
    global sq_size
    for pos in player.snake.positions:
        p = tuple(pos * sq_size)
        r = pygame.Rect(p
                        , (sq_size, sq_size))
        color = player.color
        pygame.draw.rect(screen, color, r)


def draw_obstacles(obstacles, screen):
    global sq_size
    for obstacle in obstacles:
        pos = tuple(obstacle * sq_size)
        r = pygame.Rect(pos
                        , (sq_size, sq_size))
        color = [255, 0, 0]
        pygame.draw.rect(screen, color, r)


def draw_bonuses(bonuses, screen):
    global sq_size
    for bonus in bonuses:
        center = bonus.position * sq_size + Vector(sq_size / 2, sq_size / 2)
        pygame.draw.circle(screen, bonus.color,
                           tuple(center),
                           sq_size / 2)


def draw_portal(portal, screen):
    global orange_portal
    global blue_portal
    global sq_size
    global portal_num
    pos1 = portal.position1 * sq_size
    pos2 = portal.position2 * sq_size
    if portal_num == 0:
        screen.blit(orange_portal, tuple(pos1))
        screen.blit(orange_portal, tuple(pos2))
        portal_num += 1
    else:
        screen.blit(blue_portal, tuple(pos1))
        screen.blit(blue_portal, tuple(pos2))
        portal_num = 0


def draw_text(text, color, pos, screen, center=True):
    global font
    (dx, dy) = font.size(text)
    adj_pos = pos - Vector(dx, dy) / 2 if center else pos
    screen.blit(font.render(text, False, color)
                , tuple(adj_pos))


def draw_information(players, pos, screen, remainingSteps):
    global font

    dx = Vector(60, 0)
    dy = Vector(0, 30)
    pos += dy
    for p in players:
        draw_text(str(p.score), p.color, pos, screen, center=False)
        screen.blit(player_name_images[p.name], tuple(pos + dx))
        pos += dy
    width, height = screen.get_size()
    draw_text(str(remainingSteps // 10), pygame.Color(255, 255, 255), Vector(width - 100, 30), screen, center=False)
