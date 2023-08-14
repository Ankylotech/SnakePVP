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


### Getting Started

#### Game Mechanics

The Objective of the game is to collect as many points as possible. 
This can be achieved by collecting "apples", "cherrys" or "bananas". These give more points, the longer the game goes.
Also when collected the snake grows by a tenth of the amount of points they give. 
(e.g. if the collectable gives 44 points, the snake grows by 4 tiles)
Bananas have the additional effect of halving the players points. An additional collectable is the "diamond". This turns
all snakes around.

| Collectable | starting points | change per tick | effect  |
|:-----------:|:---------------:|:---------------:|:-------:|
|    Apple    |       10        |      + 0.6      |  none   |
|   Cherry    |       10        |     * 1.005     |  none   |
|   Banana    |       10        |      + 0.3      |  HALF   |
|   Diamond   |        0        |       * 0       | REVERSE |

These values are such that apples give the most points for about 3/4 of the game, but cherries can help you 
catch up later in the game

Snakes have to avoid hitting obstacles. These can be either red blocks that are placed initially and dont move, or the tiles 
of other snakes. If a snake hits an obstacle, the points are divided by 3 and the snake is placed in a new position

To help with movement there are also portals that can teleport snakes.

#### Relevant Classes

Each AI has access to the variables mySnake, other_snakes, obstacles, bonuses, world.
They are instances of the following classes:

* mySnake: Snake
* other_snakes: List[Snake]
* obstacles: List[Vector]
* bonuses: List[Collectable]
* world: World

These provide the following important functionalities:

##### Vector

Stores an x,y position

###### Variables 

* x: X-coordinate
* y: Y-coordinate

###### Functions 

* add_direction(Direction): The vector is moved one space in a given direction

##### Snake

Manages the position and movement of a snake

###### Variables

* positions: A list of points the body of the snake is on

* direction: Direction the snake was headed in last

* lengthen: The amount of tiles the snake is currently lengthening by.
As long as this value is greater than 0 the last tile of the snake will not be removed as the snake moves

###### Functions

* head(): Gives the current position of the head of the snake

##### Collectable 

Manages items, that can be collected and give a certain score and effect. 

###### Variables

* additive: The amount of points, that are added to the score each tick

* multiplicative: The amount the score is multiplied each tick#

* score: The amount of points the collectable would give if collected at that moment

* effect: The effect that is applied once it is collected

###### Functions

* get_current_score(): Returns the points the collectable gives if collected at that moment

##### World

Manages everything in a game

###### Variables

* width: The width of the world in tiles

* height: The height of the world in tiles

* portals: The positions of the portals

###### Functions

* obstacle(position, threshold = 0): Returns whether there is an obstacle or more than the threshold snakes at the given position
* portal(position): Returns whether there is an obstacle at the given location
* occupied(position): Returns whether there is anything at the given location (obstacle, snake, portal or collectable)
* move_and_teleport(position, direction): Returns a new position after going through portals and wrapping around edges

##### Direction

Enum that can have any of the values UP, DOWN, LEFT or RIGHT

##### Apple (Collectable)

Green Collectable with a additive bonus of 0.6 and no effects

##### Cherry (Collectable)

Red Collectable with a multiplicative bonus of 0.005 and no effects

##### Banana (Collectable)

Yellow Collectable with a additive bonus of 0.3 and effect of halving the snake

##### Diamond (Collectable)

Blue Collectable with no bonus and an effect of turning every snake in the opposite direction

### Required packages

This Project builds on the following packages:

    pygame, func_timeout

both can be installed with pip

## Inspiration

* [Seekers](https://github.com/MatthiasHu/seekers) for functionality and the project overall
* [Nibbles](https://help.gnome.org/users/gnome-nibbles/stable/) for the Game
