import glob
import importlib
import os
import sys
import traceback

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
    rect_width = 16
    rect_height = 16
    screen = pygame.display.set_mode(dimensions)
    clock = pygame.time.Clock()
    random.seed(43)

    players = load_players()

    world = World(players, dimensions[0] / rect_width, dimensions[1] / rect_height)

    draw.init(world.players, rect_width, rect_height)

    game_loop(world)


def load_players():
    players = []

    if len(sys.argv) <= 1:
        for search_path in ("", "./src/ais/"):
            for filename in glob.glob(search_path + "ai*.py"):
                print(filename)
                players.append(load_player(filename))
    else:
        for filename in sys.argv[1:]:
            players.append(load_player(filename))
    print(players)
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
            seekerdef = ["def decide(mySnake, other_snakes, obstacles, collectables, world):"]
            seekerret = ["return mySnake.direction"]
            lines = seekerdef + indent(prelude + lines[1:] + seekerret)
            return "\n".join(lines)
        else:
            return code

    try:
        with open(filename, "r") as f:
            code = mogrify(f.read())
            mod = importlib.import_module(filename[:-3], 'snake')
            mod_dict = mod.__dict__
            exec(code, mod_dict)
            ai = mod.decide
            ai.is_dummy = False
    except Exception:
        print("**********************************************************", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("", file=sys.stderr)

        ai = dummy_decide
        ai.is_dummy = True

    ai.filename = filename
    ai.timestamp = os.path.getctime(filename)

    return ai


def game_loop(world):
    global screen
    global quit
    global clock

    while not quit:
        handle_events()
        world.update()
        world.draw(screen)
        clock.tick(10)


def handle_events():
    for e in pygame.event.get():
        handle_event(e)


def handle_event(e):
    if e.type == pygame.QUIT:
        global quit
        quit = True


start()
