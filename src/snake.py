# This is the main File that serves as an entrypoint for the program
import glob
import sys
import traceback
import types
import pygame
from func_timeout import func_timeout, FunctionTimedOut

import utils
from snake_types import *
from tournament import Tournament

global screen
global clock
square = 30
dimensions = (900, 900)


# Function that starts the game by loading all players and playing a tournament
def start():
    global screen
    global clock

    pygame.init()
    pygame.event.set_allowed([pygame.QUIT])
    screen = pygame.display.set_mode(dimensions)
    clock = pygame.time.Clock()
    # random.seed(42)

    players = load_players()

    tournament = Tournament(players)

    game_loop(tournament)


# Load players either from the standard location or given by arguments
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


# Load a player at a given file location
def load_player(filename):
    names = filename.split("/")
    names = names[-1].split("\\")
    name = names[-1][:-3]
    p = Player(name)
    p.ai = load_ai(filename)
    return p


# Load the AI in the file at the given location
def load_ai(filename):
    # If an AI could not be loaded, it is replaced with a dummy that only moves up
    def dummy_decide(mySnake, other_snakes, obstacles, bonuses, world):
        return Direction.UP, mySnake.memory

    def indent(lines):
        return utils.fmap(lambda l: " " + l, lines)

    # Try to wrap the Code in a function call
    def mogrify(code):
        if code.startswith("#bot"):
            prelude = []
            lines = code.split("\n")
            seekerdef = ["from snake_types import *", "def decide(mySnake, other_snakes, obstacles, bonuses, world):"]
            seekerret = ["return mySnake.direction, mySnake.memory"]
            lines = seekerdef + indent(prelude + lines[1:] + seekerret)
            return "\n".join(lines)
        else:
            raise Exception("The AI did not start with #bot")

    try:
        with open(filename, "r") as f:
            code = mogrify(f.read())
            mod = types.ModuleType(filename[:-3])
            mod_dict = mod.__dict__
            func_timeout(1
                         , exec, (code, mod_dict))
            ai = mod.decide
    except FunctionTimedOut:
        print(filename)
        print("The AI could not be loaded in time, likely an infinite loop. The AI will be replaced by a dummy", file=sys.stderr)

        ai = dummy_decide
    except Exception:
        print("Exception caused by:")
        print(filename)
        print("**********************************************************", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("The AI will now be replaced by a dummy", file=sys.stderr)

        ai = dummy_decide

    return ai


# Game Loop for playing a tournament
def game_loop(tournament):
    global screen
    global clock
    tournament.play_tournament(screen, clock, square, square, dimensions[0] // square)
    pygame.quit()


start()
