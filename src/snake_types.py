import math
from enum import Enum

from hash_color import *


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

    def dot(self, other):
        return (self.x * other.x + self.y * other.y)

    def norm(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self):
        norm = self.norm()
        if (norm == 0):
            return Vector(0, 0)
        else:
            return Vector(self.x / norm, self.y / norm)

    def add_direction(self, direction):
        if direction == Direction.UP:
            return self + Vector(0,-1)
        elif direction == Direction.DOWN:
            return self + Vector(0,1)
        elif direction == Direction.LEFT:
            return self + Vector(-1,0)
        else:
            return self + Vector(1,0)

    def rotated(self):
        return Vector(-self.y, self.x)

    def fmap(self, f):
        return Vector(f(self.x), f(self.y))


class Direction(Enum):
    UP, DOWN, LEFT, RIGHT = range(4)


class Snake:
    def __init__(self, positions, direction):
        self.positions = positions
        self.direction = direction
        self.lengthen = 0

    def move(self, width, height):
        head = Vector(self.positions[0].x,self.positions[0].y).add_direction(self.direction)
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


class Player:
    def __init__(self, name):
        self.name = name
        self.color = string_hash_color(name)
        self.score = 0
        self.snake = Snake([], Direction.UP)


class Collectable:
    additive = 0
    multiplicative = 1
    color = [0,0,0]

    def __init__(self, world):
        self.position = world.random_free()
        self.effect = 1

    def new_position(self, world):
        self.position = world.random_free()

    def collect(self, world):
        self.new_position(world)
        self.effect += self.additive
        self.effect *= self.multiplicative
        return self.effect


class Apple(Collectable):
    additive = 5
    color = [0,255,0]
