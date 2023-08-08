#bot
ind = 2
if bonuses[ind].position.x < mySnake.positions[0].x:
    if world.obstacle(mySnake.positions[0].add_direction(Direction.LEFT)):
        if bonuses[ind].position.y > mySnake.positions[0].y:
            mySnake.direction = Direction.DOWN
        else:
            mySnake.direction = Direction.UP
    else:
        mySnake.direction = Direction.LEFT
elif bonuses[ind].position.x > mySnake.positions[0].x:
    if world.obstacle(mySnake.positions[0].add_direction(Direction.RIGHT)):
        if bonuses[ind].position.y > mySnake.positions[0].y:
            mySnake.direction = Direction.DOWN
        else:
            mySnake.direction = Direction.UP
    else:
        mySnake.direction = Direction.RIGHT
elif bonuses[ind].position.y < mySnake.positions[0].y:
    if world.obstacle(mySnake.positions[0].add_direction(Direction.UP)):
        if bonuses[ind].position.x > mySnake.positions[0].x:
            mySnake.direction = Direction.RIGHT
        else:
            mySnake.direction = Direction.LEFT
    else:
        mySnake.direction = Direction.UP
else:
    if world.obstacle(mySnake.positions[0].add_direction(Direction.DOWN)):
        if bonuses[ind].position.x > mySnake.positions[0].x:
            mySnake.direction = Direction.RIGHT
        else:
            mySnake.direction = Direction.LEFT
    else:
        mySnake.direction = Direction.DOWN
