import draw
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
        player.snake.positions.append(pos)
        player.snake.direction = Direction.RIGHT
        player.snake.lengthen = 4
        for _ in range(4):
            player.snake.move(self.width, self.height)

    def obstacle(self, pos):
        for obstacle in self.obstacles:
            if obstacle is pos:
                return True
        for player in self.players:
            for position in player.snake.positions:
                if pos is position:
                    return True
        return False

    def occupied(self, pos):
        for obstacle in self.obstacles:
            if obstacle is pos:
                return True
        for player in self.players:
            for position in player.snake.positions:
                if pos is position:
                    return True
        for collectable in self.collectables:
            if collectable.position is pos:
                return True
        return False

    def update(self):
        for player in self.players:
            player.snake.move(self.width, self.height)

    def draw(self, screen):
        draw.draw(self.players, self.obstacles, self.collectables, screen)
