import glob
import importlib
import os
import sys
import traceback
import types

import pygame

import draw
import utils
from snake_types import *
from world import World

global screen
global clock
global quit
quit = False


def start():
    global screen
    global clock

    pygame.init()
    pygame.event.set_allowed([pygame.QUIT])
    dimensions = (800, 800)
    sq_size = 16
    screen = pygame.display.set_mode(dimensions)
    clock = pygame.time.Clock()
    random.seed(43)

    players = load_players()

    world = World(players, dimensions[0] / sq_size, dimensions[1] / sq_size)

    draw.init(world.players, sq_size)

    game_loop(world)


def load_players():
    players = []

    if len(sys.argv) <= 1:
        for search_path in ("", "ais/"):
            for filename in glob.glob(search_path + "ai*.py"):
                players.append(load_player(filename))
    else:
        for filename in sys.argv[1:]:
            players.append(load_player(filename))
    return players


def load_player(filename):
    name = filename[:-3]
    p = Player(name)
    p.ai = load_ai(filename)
    return p


def load_ai(filename):
    def dummy_decide(mySnake, other_snakes, obstacles, collectables, world):
        return Direction.UP

    def indent(lines):
        return utils.fmap(lambda l: " " + l, lines)

    def mogrify(code):
        if code.startswith("#bot"):
            prelude = []
            lines = code.split("\n")
            seekerdef = ["from snake_types import *","def decide(mySnake, other_snakes, obstacles, collectables, world):"]
            seekerret = ["return mySnake.direction"]
            lines = seekerdef + indent(prelude + lines[1:] + seekerret)
            return "\n".join(lines)
        else:
            return code

    try:
        with open(filename, "r") as f:
            code = mogrify(f.read())
            mod = types.ModuleType(filename[:-3])
            mod_dict = mod.__dict__
            exec(code, mod_dict)
            ai = mod.decide
    except Exception:
        print("**********************************************************", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("", file=sys.stderr)

        ai = dummy_decide

    return ai


def game_loop(world):
    global screen
    global quit
    global clock
    step = 0
    print(quit)
    while not quit and step <= 1000:
        handle_events()
        world.update()
        world.draw(screen)
        clock.tick(10)
        step += 1
    print("the winner is: " + world.get_winner())


def handle_events():
    for e in pygame.event.get():
        handle_event(e)


def handle_event(e):
    if e.type == pygame.QUIT:
        global quit
        quit = True


start()
