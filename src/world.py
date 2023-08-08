import copy
import sys
import traceback

import pygame

import draw
from snake_types import *
from func_timeout import func_timeout, FunctionTimedOut


class World:
    def __init__(self, players, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
        self.portals = []
        self.players = players
        self.boni = []
        self.obstacles = self.generate_obstacles()
        self.portals = self.generate_portals(2)
        self.boni.append(Apple(self))
        self.boni.append(Cherry(self))
        self.boni.append(Banana(self))
        self.boni.append(Diamond(self))
        for p in players:
            p.score = 0
            self.position_player(p)

    def random_free(self):
        pos = Vector(random.randint(0, self.width-1), random.randint(0, self.height-1))
        while self.occupied(pos):
            pos = Vector(random.randint(0, self.width-1), random.randint(0, self.height-1))
        return pos

    def generate_obstacles(self):
        list = []

        while random.uniform(0, 1) < 0.8:
            list.append(self.random_free())

        return list

    def generate_portals(self, num):
        result = []
        for _ in range(num):
            pos1 = self.random_free()
            pos2 = self.random_free()
            result.append(Portal(pos1, pos2))
        return result

    def right(self, pos1, n):
        result = pos1 + Vector(n, 0)
        result.x %= self.width
        return result

    def position_player(self, player):
        pos = self.random_free()
        while self.occupied(self.right(pos, 1)) or self.occupied(self.right(pos, 2)) or self.occupied(
                self.right(pos, 3)) or self.occupied(self.right(pos, 4)):
            pos = self.random_free()
        player.snake.positions = [pos]
        player.snake.direction = Direction.RIGHT
        player.snake.lengthen = 4
        for _ in range(4):
            player.snake.move(self.width, self.height)

    def obstacle(self, pos):
        for obstacle in self.obstacles:
            if obstacle is pos:
                continue
            if obstacle == pos:
                return True
        for player in self.players:
            for position in player.snake.positions:
                if position is pos:
                    continue
                if pos == position:
                    return True
        return False

    def portal(self, pos):
        for portal in self.portals:
            if portal.position1 is pos or portal.position2 is pos:
                continue
            if portal.position1 == pos or portal.position2 == pos:
                return True
        return False

    def occupied(self, pos):
        if self.obstacle(pos) or self.portal(pos):
            return True
        for bonus in self.boni:
            if bonus is pos:
                continue
            if bonus.position == pos:
                return True
        return False

    def ai_calcs(self):
        for player in self.players:
            otherSnakes = copy.deepcopy([p.snake for p in self.players if p is not player])
            world = copy.deepcopy(self)
            try:
                direction = func_timeout(0.1, player.ai, (copy.deepcopy(player.snake), otherSnakes, world.obstacles, world.boni, world))
            except FunctionTimedOut:
                print("The AI of Player "
                      + player.name
                      + " took to long to complete and was canceled")
                direction = player.snake.direction
            except Exception as e:
                print("The AI of Player "
                      + player.name
                      + " raised an exception:")
                traceback.print_exc(file=sys.stderr)
                direction = player.snake.direction
            player.snake.direction = Direction(direction)

    def update(self, tick):
        self.ai_calcs()
        for player in self.players:
            player.snake.move(self.width, self.height)

        for player in self.players:
            position = player.snake.positions[0]
            for portal in self.portals:
                if position == portal.position1:
                    player.snake.positions[0] = copy.copy(portal.position2)
                if position == portal.position2:
                    player.snake.positions[0] = copy.copy(portal.position1)

        reset = []
        for player in self.players:
            if self.obstacle(player.snake.positions[0]):
                reset.append(player)

        for player in reset:
            player.score = int(player.score / 3)
            self.position_player(player)

        reverse = 0
        for player in self.players:
            for bonus in self.boni:
                if player.snake.positions[0] == bonus.position:
                    value, effect = bonus.collect(self, tick)
                    if effect == Effect.REGULAR:
                        player.score += value
                        player.snake.lengthen = math.ceil(value / 10)
                    elif effect == Effect.HALF:
                        player.score += value
                        mid = math.ceil(len(player.snake.positions) / 2)
                        player.snake.positions = player.snake.positions[:mid]
                    elif effect == Effect.REVERSE:
                        reverse += 1

        if reverse % 2 == 1:
            for player in self.players:
                player.snake.positions.reverse()

    def draw(self, screen):
        draw.draw(self.players, self.obstacles, self.boni, self.portals, screen)

    def get_winner(self):
        max = self.players[0].score
        win = self.players[0].name
        for player in self.players:
            if player.score > max:
                max = player.score
                win = player.name
        return win

    def simulate(self):
        step = 0
        while step < 1000:
            self.update(step)
            step += 1

    def simulate_and_show(self, screen, clock, size):
        global done
        done = False
        draw.init(self.players, size)
        step = 0
        while step <= 1000:
            handle_events()
            self.update(step)
            self.draw(screen)
            clock.tick(10)
            step += 1


def handle_events():
    for e in pygame.event.get():
        handle_event(e)


def handle_event(e):
    if e.type == pygame.QUIT:
        pygame.quit()
        exit()
