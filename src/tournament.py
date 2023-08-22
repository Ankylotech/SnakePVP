from random import shuffle
import pygame
from pygame.locals import *
from itertools import combinations

from snake_types import Vector
from world import World

simulate = False
num_rounds = 8


background_color = [0, 0, 30]


# Class for managing a snake game tournament
class Tournament:
    # Initialize tournament and split if necessary
    def __init__(self, players, final=True):
        self.players = [[x, 0, 0] for x in players]
        shuffle(self.players)
        self.final = final
        self.ranked = False
        games = list(combinations(range(len(self.players)), 2))

        games.sort(key = lambda game: game[0] - game[1])
        self.games = [(self.players[x[0]], self.players[x[1]]) for x in games for _ in range(num_rounds)]

    # Play the full tournament
    def play_tournament(self, screen, clock, width, height, size):
        self.show_bracket(screen, width * size, height * size, size)
        while len(self.games) > 0:
            self.play_next(screen, clock, width, height, size)
            k = len(self.players) * 2
            self.players.sort(key=lambda p: (p[1]+1) * k - p[2], reverse=True)
            if not simulate:
                self.show_bracket(screen, width * size, height * size, size)

        self.show_bracket(screen, width * size, height * size, size)
        print("final scores")
        for p in self.players:
            print(p[0].name + ":" + str(p[1]) + " | " + str(p[2]))

    # Play the last layer of tournament games that have not been played yet
    def play_next(self, screen, clock, width, height, size):
        game = self.games.pop()
        p1 = game[0][0]
        p2 = game[1][0]
        world = World([p1, p2], width, height)
        if simulate:
            world.simulate()
        else:
            world.simulate_and_show(screen, clock, size)
        game[0][2] += 1
        game[1][2] += 1
        if p1.score > p2.score:
            game[0][1] += p1.score
        elif p2.score > p1.score:
            game[1][1] += p2.score
        else:
            game[0][1] += p1.score // 2
            game[1][1] += p2.score // 2

    # Show the current bracket of games played and to be played
    def show_bracket(self, screen, width, height, sq_size):
        screen.fill(background_color)
        font = pygame.font.SysFont("monospace", (sq_size * 20)//32, bold=True)
        pos = Vector(2*width/3, height/2 - ((len(self.players)+1)/2)*30)
        text = "name : points | games"
        (dx, dy) = font.size(text)
        adj_pos = pos - Vector(dx, 0)
        screen.blit(font.render(text, False, pygame.Color(255, 255, 255))
                    , tuple(adj_pos))
        pos += Vector(0, dy)
        for k in self.players:
            text = k[0].name + ": " + str(k[1]).ljust(6) + " | " + str(k[2]).ljust(5)
            (dx, dy) = font.size(text)
            adj_pos = pos - Vector(dx,0)
            screen.blit(font.render(text, False, k[0].color)
                        , tuple(adj_pos))
            pos += Vector(0, dy)
        font = pygame.font.SysFont("monospace", (sq_size * 40)//32, bold=True)
        text = "Press any key to continue"
        (dx, dy0) = font.size(text)
        screen.blit(font.render(text, False, pygame.Color(255, 255, 255))
                    , (width // 2 - dx / 2, height - 3 * dy))
        if len(self.games) > 0:
            font = pygame.font.SysFont("monospace", (sq_size * 20)//32, bold=True)
            game = self.games[-1]
            text = "Next game: " + str(game[0][0].name) + " vs " + str(game[1][0].name)
            (dx, dy) = font.size(text)
            screen.blit(font.render(text, False, pygame.Color(255, 255, 255))
                        , (width // 2 - dx/2, height - 2 * dy - 3 * dy0))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    return
