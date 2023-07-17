import glob
import sys
import traceback
import types

import pygame


import utils
from snake_types import *
from tournament import Tournament

global screen
global clock
global dimensions
sq_size = 32


def start():
    global screen
    global clock
    global dimensions

    pygame.init()
    pygame.event.set_allowed([pygame.QUIT])
    dimensions = (960, 960)
    screen = pygame.display.set_mode(dimensions)
    clock = pygame.time.Clock()
    # random.seed(44)

    players = load_players()

    tournament = Tournament(players)

    game_loop(tournament)


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
    def dummy_decide(mySnake, other_snakes, obstacles, boni, world):
        return Direction.UP

    def indent(lines):
        return utils.fmap(lambda l: " " + l, lines)

    def mogrify(code):
        if code.startswith("#bot"):
            prelude = []
            lines = code.split("\n")
            seekerdef = ["from snake_types import *", "def decide(mySnake, other_snakes, obstacles, boni, world):"]
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
        print(filename)
        print("**********************************************************", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("", file=sys.stderr)

        ai = dummy_decide

    return ai


def game_loop(tournament):
    global screen
    global clock
    global dimensions
    tournament.play_tournament(screen,clock, dimensions[0] / sq_size, dimensions[1] / sq_size, sq_size)
    pygame.quit()


start()
