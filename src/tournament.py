import copy
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
            if self.left.play_last(screen, clock, width, height, size) and self.right.play_last(screen, clock, width, height, size):
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
        self.show_scores(screen)
        font = pygame.font.SysFont("monospace", 40, bold=True)
        screen.blit(font.render("Press any key to continue", False, pygame.Color(255, 255, 255))
                    , (width//2 - 300, height - 60))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    return

    def show_scores(self, screen, x=0, y=0, width=-1, height=-1):
        if width == -1:
            width, height = screen.get_size()
        dx = Vector(200, 0)
        dy = Vector(0, 30)
        if self.split:
            self.left.show_scores(screen, x + dx.x, y, width - dx.x, height / 2)
            self.right.show_scores(screen, x + dx.x, y + height / 2, width - dx.x, height / 2)

        if len(self.players) == 0:
            pos = Vector(x + 10, y + height / 2 - dy.y * self.group_size / 2)

            for i in range(self.group_size):
                k = i % (self.group_size // 2)
                text = str(k+1) + ". from "
                if k != i:
                    text += "lower "
                else:
                    text += "upper "
                text += "bracket"
                font = pygame.font.SysFont("monospace", 20, bold=True)
                screen.blit(font.render(text, False, pygame.Color(255, 255, 255))
                            , tuple(pos))
                pos += dy
        else:
            pos = Vector(x, y + height / 2 - dy.y * len(self.players) / 2)

            for p in self.players:
                text = str(p.score) + "  " + p.name
                font = pygame.font.SysFont("monospace", 20, bold=True)
                screen.blit(font.render(text, False, p.color)
                            , tuple(pos))
                pos += dy





