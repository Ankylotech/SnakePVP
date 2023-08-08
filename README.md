# SnakeAIChallenge

Artificial intelligence programing challenge 

AIs compete to collect the most points in a snake-like game 

## Usage 

    python3 src/snake.py [AI locations]

* AI locations: The locations for the files containing AI challengers, default is looking for all ai*.py files in src/ais

### AI files

Inside a File that is used for a challenger you have Access to the variables 

    mySnake, other_snakes, obstacles, bonuses, world 

In the end mySnake.direction must be set to one of the values 

    Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT

The snake will choose to go that direction next turn

## Required packages

This Project builds on the following packages:

    pygame, func_timeout

both can be installed with pip

## Inspiration

* [Seekers](https://github.com/MatthiasHu/seekers) for functionality and the project overall
* [Nibbles](https://help.gnome.org/users/gnome-nibbles/stable/) for the Game
