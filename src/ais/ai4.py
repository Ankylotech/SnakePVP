#bot
if bonuses[0].position.x < mySnake.positions[0].x:
    if world.obstacle(mySnake.positions[0].add_direction(Direction.LEFT)):
        if bonuses[0].position.y > mySnake.positions[0].y:
            mySnake.direction = Direction.DOWN
        else:
            mySnake.direction = Direction.UP
    else:
        mySnake.direction = Direction.LEFT
elif bonuses[0].position.x > mySnake.positions[0].x:
    if world.obstacle(mySnake.positions[0].add_direction(Direction.RIGHT)):
        if bonuses[0].position.y > mySnake.positions[0].y:
            mySnake.direction = Direction.DOWN
        else:
            mySnake.direction = Direction.UP
    else:
        mySnake.direction = Direction.RIGHT
elif bonuses[0].position.y < mySnake.positions[0].y:
    if world.obstacle(mySnake.positions[0].add_direction(Direction.UP)):
        if bonuses[0].position.x > mySnake.positions[0].x:
            mySnake.direction = Direction.RIGHT
        else:
            mySnake.direction = Direction.LEFT
    else:
        mySnake.direction = Direction.UP
else:
    if world.obstacle(mySnake.positions[0].add_direction(Direction.DOWN)):
        if bonuses[0].position.x > mySnake.positions[0].x:
            mySnake.direction = Direction.RIGHT
        else:
            mySnake.direction = Direction.LEFT
    else:
        mySnake.direction = Direction.DOWN
