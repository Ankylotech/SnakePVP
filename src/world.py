import draw
import copy
from snake_types import *


class World:
    def __init__(self, players, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
        self.players = players
        self.collectables = []
        self.obstacles = self.generate_obstacles()
        self.collectables.append(Apple(self))
        for p in players:
            self.position_player(p)

    def random_free(self):
        pos = Vector(int(random.uniform(0, self.width)), int(random.uniform(0, self.height)))
        while self.occupied(pos):
            pos = Vector(int(random.uniform(0, self.width)), int(random.uniform(0, self.height)))
        return pos

    def generate_obstacles(self):
        list = []

        while random.uniform(0, 1) < 0.8:
            list.append(self.random_free())

        return list

    def position_player(self, player):
        pos = self.random_free()
        while self.occupied(pos + Vector(1, 0)) or self.occupied(pos + Vector(2, 0)) or self.occupied(pos + Vector(3, 0)) or self.occupied(pos + Vector(4, 0)):
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

    def occupied(self, pos):
        if self.obstacle(pos):
            return True
        for collectable in self.collectables:
            if collectable is pos:
                continue
            if collectable.position == pos:
                return True
        return False

    def ai_calcs(self):
        for player in self.players:
            otherSnakes = copy.deepcopy([p.snake for p in self.players if p is not player])
            world = copy.deepcopy(self)
            direction = player.ai(copy.deepcopy(player.snake), otherSnakes, world.obstacles, world.collectables, world)
            player.snake.direction = Direction(direction)

    def update(self):
        self.ai_calcs()
        for player in self.players:
            player.snake.move(self.width, self.height)
        reset = []
        for player in self.players:
            if self.obstacle(player.snake.positions[0]):
                reset.append(player)

        for player in reset:
            player.score = int(player.score / 3)
            self.position_player(player)

        for player in self.players:
            for collect in self.collectables:
                if player.snake.positions[0] == collect.position:
                    value = collect.collect(self)
                    player.score += value
                    player.snake.lengthen = math.ceil(value/10)

    def draw(self, screen):
        draw.draw(self.players, self.obstacles, self.collectables, screen)

    def get_winner(self):
        max = self.players[0].score
        win = self.players[0].name
        for player in self.players:
            if player.score > max:
                max = player.score
                win = player.name
        return win
