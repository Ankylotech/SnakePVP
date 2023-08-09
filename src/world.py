import copy
import sys
import traceback

import pygame
from func_timeout import func_timeout, FunctionTimedOut

import draw
from snake_types import *


class World:
    def __init__(self, players, width, height):
        self.width = width
        self.height = height
        self.obstacleMap = [[False] * width for _ in range(height)]
        self.obstacles = []
        self.portals = []
        self.players = players
        self.bonuses = []
        self.snakeCounts = [[0] * self.width for _ in range(self.height)]
        self.generate_obstacles()
        self.portals = self.generate_portals(2)
        self.bonuses.append(Apple(self))
        self.bonuses.append(Cherry(self))
        self.bonuses.append(Banana(self))
        self.bonuses.append(Diamond(self))
        for p in players:
            p.score = 0
            self.position_player(p)

    def random_free(self):
        pos = Vector(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        while self.occupied(pos):
            pos = Vector(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return pos

    def generate_obstacles(self):
        while random.uniform(0, 1) < 0.8:
            pos = self.random_free()
            self.obstacleMap[pos.x][pos.y] = True
            self.obstacles.append(pos)

    def generate_portals(self, num):
        result = []
        for _ in range(num):
            pos1 = self.random_free()
            pos2 = self.random_free()
            result.append(Portal(pos1, pos2))
        return result

    def right(self, pos1, n):
        result = pos1 + Vector(n, 0)
        result.x = result.x % self.width
        return result

    def position_player(self, player):
        for p in player.snake.positions:
            self.snakeCounts[p.x][p.y] -= 1
        pos = self.random_free()
        while self.occupied(self.right(pos, 1)) or self.occupied(self.right(pos, 2)) or self.occupied(
                self.right(pos, 3)) or self.occupied(self.right(pos, 4)):
            pos = self.random_free()
        player.snake.positions = [pos]
        player.snake.direction = Direction.RIGHT
        player.snake.lengthen = 4
        self.snakeCounts[pos.x][pos.y] += 1
        for i in range(4):
            player.snake.move(self.width, self.height)
            self.snakeCounts[self.right(pos, i + 1).x][pos.y] += 1

    def obstacle(self, pos, threshold=0):
        return self.obstacleMap[pos.x][pos.y] or self.snakeCounts[pos.x][pos.y] > threshold

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
        for bonus in self.bonuses:
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
                direction = func_timeout(0.1, player.ai, (
                copy.deepcopy(player.snake), otherSnakes, world.obstacles, world.bonuses, world))
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

        self.snakeCounts = [[0] * self.width for _ in range(self.height)]
        for player in self.players:

            player.snake.move(self.width, self.height)

            position = player.snake.head()
            for portal in self.portals:
                if position == portal.position1:
                    player.snake.positions[0] = copy.copy(portal.position2)
                if position == portal.position2:
                    player.snake.positions[0] = copy.copy(portal.position1)
            for pos in player.snake.positions:
                self.snakeCounts[pos.x][pos.y] += 1

        reset = []
        for player in self.players:
            if self.obstacle(player.snake.head(), 1):
                reset.append(player)

        for player in reset:
            player.score = int(player.score / 3)
            self.position_player(player)

        reverse = 0
        for bonus in self.bonuses:
            bonus.update()
            for player in self.players:
                if player.snake.head() == bonus.position:
                    value, effect = bonus.collect(self, tick)
                    if effect == Effect.REGULAR:
                        player.score += value
                        player.snake.lengthen = value // 10
                    elif effect == Effect.HALF:
                        player.score += value
                        mid = math.ceil((len(player.snake.positions) + player.snake.lengthen) / 2)
                        if player.snake.lengthen < len(player.snake.positions):
                            player.snake.positions = player.snake.positions[:mid]
                            player.snake.lengthen = 0
                        else:
                            player.snake.lengthen -= mid
                    elif effect == Effect.REVERSE:
                        reverse += 1

        if reverse % 2 == 1:
            for player in self.players:
                player.snake.positions.reverse()

    def draw(self, screen, remainingSteps):
        draw.draw(self.players, self.obstacles, self.bonuses, self.portals, screen, remainingSteps)

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
        draw.init(self.players, size)
        step = 0
        while step <= 1000:
            handle_events()
            self.update(step)
            self.draw(screen, 1000 - step)
            clock.tick(10)
            step += 1


def handle_events():
    for e in pygame.event.get():
        handle_event(e)


def handle_event(e):
    if e.type == pygame.QUIT:
        pygame.quit()
        exit()
