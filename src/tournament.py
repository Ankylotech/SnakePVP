import copy
import random

import pygame
from pygame.locals import *

from snake_types import Vector
from world import World

background_color = [0, 0, 30]


class Tournament:
    def __init__(self, players, group_size=4, sub=False, final=True):
        self.players = []
        self.group_size = group_size
        self.sub = sub
        self.ranked = False
        self.final = final
        random.shuffle(players)
        if len(players) > group_size:
            self.split = True
            self.left = Tournament(players[:len(players) // 2], group_size, True, False)
            self.right = Tournament(players[len(players) // 2:], group_size, True, False)
        else:
            self.players = players
            self.split = False

    def play_tournament(self, screen, clock, width, height, size):
        if self.split:
            self.show_bracket(screen)
        while not self.play_last(screen, clock, width, height, size):
            if self.split:
                self.show_bracket(screen)
        self.players.sort(key=lambda p: p.score, reverse=True)
        print("final scores")
        for p in self.players:
            print(p.name + ":" + str(p.score))
        if self.split:
            self.show_bracket(screen)

    def play_last(self, screen, clock, width, height, size):
        if self.split and not self.left.ranked:
            if self.left.play_last(screen, clock, width, height, size) and self.right.play_last(screen, clock, width,
                                                                                                height, size):
                self.left.players.sort(key=lambda p: p.score, reverse=True)
                self.right.players.sort(key=lambda p: p.score, reverse=True)
                first_half = copy.deepcopy(self.left.players[:self.group_size // 2])
                second_half = copy.deepcopy(self.right.players[:self.group_size // 2])
                self.players = first_half + second_half
                for player in self.players:
                    player.score = 0
                self.ranked = True
            return False
        else:
            if len(self.players) > self.group_size // 2 or self.final:
                world = World(self.players, width, height)
                world.simulate_and_show(screen, clock, size)
            self.ranked = True
            return True

    def show_bracket(self, screen):
        width, height = screen.get_size()
        screen.fill(background_color)
        space = (width - self.total_max_text()) / (self.total_depth() + 1)
        self.show_scores(screen, space, space, 0, width, height)
        font = pygame.font.SysFont("monospace", 40, bold=True)
        screen.blit(font.render("Press any key to continue", False, pygame.Color(255, 255, 255))
                    , (width // 2 - 300, height - 60))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    return

    def total_max_text(self):
        total = 0
        if self.split:
            total = max(self.left.total_max_text(), self.right.total_max_text())

        font = pygame.font.SysFont("monospace", 20, bold=True)
        if len(self.players) == 0:
            total += font.size(str(self.group_size) + ". from upper bracket")[0]
        else:
            maxName = ""
            for p in self.players:
                if len(p.name + str(p.score)) > len(maxName):
                    maxName = p.name + str(p.score)
            total += font.size(maxName + ": ")[0]
        return total

    def total_depth(self):
        if self.split:
            return self.left.total_depth() + 1
        else:
            return 1

    def show_scores(self, screen, space, x, y, width, height):
        if width == -1:
            width, height = screen.get_size()
        font = pygame.font.SysFont("monospace", 20, bold=True)

        dx = Vector(0, 0)
        dy = Vector(0, 30)
        if len(self.players) == 0:
            pos = Vector(x, y + height / 2 - dy.y * self.group_size / 2)

            for i in range(self.group_size):
                k = i % (self.group_size // 2)
                text = str(k + 1) + ". from "
                if k != i:
                    text += "lower "
                else:
                    text += "upper "
                text += "bracket"
                if font.size(text)[0] > dx.x:
                    dx.x = font.size(text)[0]
                screen.blit(font.render(text, False, pygame.Color(255, 255, 255))
                            , tuple(pos))
                pos += dy
        else:
            pos = Vector(x, y + height / 2 - dy.y * len(self.players) / 2)
            maxName = 0
            for p in self.players:
                if len(p.name) > maxName:
                    maxName = len(p.name)

            for p in self.players:
                text = p.name.ljust(maxName) + ": " + str(p.score)
                if font.size(text)[0] > dx.x:
                    dx.x = font.size(text)[0]
                screen.blit(font.render(text, False, p.color)
                            , tuple(pos))
                pos += dy
        dx.x += space
        if self.split:
            self.left.show_scores(screen, space, x + dx.x, y, width - dx.x, height / 2)
            self.right.show_scores(screen, space, x + dx.x, y + height / 2, width - dx.x, height / 2)
