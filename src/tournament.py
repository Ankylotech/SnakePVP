import copy
import random
import pygame
from pygame.locals import *

from snake_types import Vector
from world import World

background_color = [0, 0, 30]


# Class for managing a snake game tournament
class Tournament:
    # Initialize tournament and split if necessary
    def __init__(self, players, group_size=4, final=True):
        self.players = []
        self.group_size = group_size
        self.final = final
        self.ranked = len(players) == group_size / 2
        if len(players) > group_size:
            self.split = True
            self.left = Tournament(players[:len(players) // 2], group_size, False)
            self.right = Tournament(players[len(players) // 2:], group_size, False)
        else:
            self.players = players
            self.split = False

    # Play the full tournament
    def play_tournament(self, screen, clock, width, height, size):
        if self.split:
            self.show_bracket(screen)
        while not self.ranked:
            self.play_last(screen, clock, width, height, size)
            if self.split:
                self.show_bracket(screen)
        self.players.sort(key=lambda p: p.score, reverse=True)
        print("final scores")
        for p in self.players:
            print(p.name + ":" + str(p.score))
        if self.split:
            self.show_bracket(screen)

    def non_ranked_depth(self):
        if self.ranked:
            return 0
        if not self.split:
            return 1
        return max(self.left.non_ranked_depth(), self.right.non_ranked_depth()) + 1

    # Play the last layer of tournament games that have not been played yet
    def play_last(self, screen, clock, width, height, size):
        if self.split and not (self.left.ranked and self.right.ranked) and not self.ranked:
            if self.left.non_ranked_depth() < self.right.non_ranked_depth():
                self.right.play_last(screen, clock, width, height, size)
            else:
                self.left.play_last(screen, clock, width, height, size)
            if self.left.ranked and self.right.ranked:
                first_half = copy.deepcopy(self.left.players[:self.group_size // 2])
                second_half = copy.deepcopy(self.right.players[:self.group_size // 2])
                self.players = first_half + second_half
                for player in self.players:
                    player.score = 0
        else:
            if (len(self.players) > self.group_size // 2 or self.final) and not self.ranked:
                world = World(self.players, width, height)
                world.simulate_and_show(screen, clock, size)
                self.players.sort(key=lambda p: p.score, reverse=True)
                print("Scores:")
                for p in self.players:
                    print(p.name + ":" + str(p.score))
            self.ranked = True

    # Show the current bracket of games played and to be played
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

    # total length of texts in the tournament bracket
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

    # Total depth of games to be played
    def total_depth(self):
        if self.split:
            return max(self.left.total_depth(), self.right.total_depth()) + 1
        else:
            return 1

    # Show the Bracket scores
    def show_scores(self, screen, space, x, y, width, height, active=True):
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
            if self.ranked:
                active = False
            right_active = self.left.non_ranked_depth() < self.right.non_ranked_depth()
            self.left.show_scores(screen, space, x + dx.x, y, width - dx.x, height / 2, active and not right_active)
            self.right.show_scores(screen, space, x + dx.x, y + height / 2, width - dx.x, height / 2, active and right_active)

        if active and not self.ranked and (not self.split or (self.split and self.left.ranked and self.right.ranked)):
            start = (x, y + height / 2 + dy.y * len(self.players) / 2)
            end = (x + dx.x - space, y + height / 2 + dy.y * len(self.players) / 2)
            pygame.draw.line(screen, (255, 0, 0), start, end, 2)
