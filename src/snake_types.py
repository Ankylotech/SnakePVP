from enum import Enum

from hash_color import *


# Vector class for storing positions
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def is_vector(obj):
        return isinstance(obj, Vector)

    def __iter__(self):
        return (self.x, self.y).__iter__()

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise IndexError

    def __add__(left, right):
        return Vector(left.x + right.x, left.y + right.y)

    def __sub__(left, right):
        return Vector(left.x - right.x, left.y - right.y)

    def __neg__(self):
        return self * (-1)

    def __mul__(self, factor):
        return Vector(self.x * factor, self.y * factor)

    def __rmul__(self, factor):
        return Vector(self.x * factor, self.y * factor)

    def __truediv__(self, divisor):
        return self * (1 / divisor)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "Vector(" + str(self.x) + ", " + str(self.y) + ")"

    def add_direction(self, direction):
        if direction == Direction.UP:
            return self + Vector(0, -1)
        elif direction == Direction.DOWN:
            return self + Vector(0, 1)
        elif direction == Direction.LEFT:
            return self + Vector(-1, 0)
        else:
            return self + Vector(1, 0)

    def rotated(self):
        return Vector(-self.y, self.x)

    def fmap(self, f):
        return Vector(f(self.x), f(self.y))

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


# The 4 directions a snake can move
class Direction(Enum):
    UP, DOWN, LEFT, RIGHT = range(4)


# Snake class for managing movement and position if a snake
class Snake:
    def __init__(self, positions, direction):
        self.positions = positions
        self.direction = direction
        self.lengthen = 0

    def move(self, width, height):
        head = self.head().add_direction(self.direction)
        if head.y < 0:
            head.y = height - 1
        if head.y == height:
            head.y = 0
        if head.x < 0:
            head.x = width - 1
        if head.x == width:
            head.x = 0

        self.positions = [head] + self.positions
        if self.lengthen == 0:
            self.positions.pop()
        else:
            self.lengthen -= 1

    def head(self):
        return self.positions[0]


# Player class for managing player ais and snakes
class Player:
    def __init__(self, name):
        self.name = name
        self.color = string_hash_color(name)
        self.score = 0
        self.snake = Snake([], Direction.UP)


# Enum for managing the different effect a Bonus can have
class Effect(Enum):
    REGULAR, HALF, REVERSE = range(3)


# Class for managing collectables in the game
class Collectable:
    additive = 0
    multiplicative = 1
    color = [0, 0, 0]
    effect = Effect.REGULAR
    score = 10

    def __init__(self, world):
        self.position = world.random_free()

    def new_position(self, world):
        self.position = world.random_free()

    def collect(self, world):
        self.new_position(world)
        return self.get_current_score(), self.effect

    def get_current_score(self):
        return int(self.score)

    def update(self):
        self.score += self.additive
        self.score *= self.multiplicative


class Apple(Collectable):
    additive = 0.6
    color = [0, 255, 0]


class Cherry(Collectable):
    multiplicative = 1.005
    color = [255, 0, 0]


class Banana(Collectable):
    additive = 0.3
    color = [255, 255, 0]
    effect = Effect.HALF


class Diamond(Collectable):
    multiplicative = 0
    color = [200, 200, 255]
    effect = Effect.REVERSE


class Portal:
    def __init__(self, position1, position2):
        self.position1 = position1
        self.position2 = position2
