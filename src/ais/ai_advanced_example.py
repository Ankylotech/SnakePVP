#bot
# ^ So muss jede Datei starten

# Ziel des Bots:
# Berechne für jedes Collectable den Score pro verwendeter Zeit um dorthin zu gelangen
# und gehe zu dem mit dem größten "Mehrwert"

dist = [[(world.width * world.height * 100, Direction.UP) for _ in range(world.width)] for _ in range(world.height)]
position = mySnake.head()
dist[position.x][position.y] = (0, Direction.UP)
current = []
up = world.move_and_teleport(position, Direction.UP)
down = world.move_and_teleport(position, Direction.DOWN)
left = world.move_and_teleport(position, Direction.LEFT)
right = world.move_and_teleport(position, Direction.RIGHT)

if not world.obstacle(up):
    dist[up.x][up.y] = (1, Direction.UP)
    current.append(up)

if not world.obstacle(down):
    dist[down.x][down.y] = (1, Direction.DOWN)
    current.append(down)

if not world.obstacle(left):
    dist[left.x][left.y] = (1, Direction.LEFT)
    current.append(left)

if not world.obstacle(right):
    dist[right.x][right.y] = (1, Direction.RIGHT)
    current.append(right)

while len(current) > 0:
    now = current.pop()
    cur_dist, cur_dir = dist[now.x][now.y]
    for d in Direction:
        next = world.move_and_teleport(now, d)
        if not world.obstacle(next):
            dst, direction = dist[next.x][next.y]
            if dst > cur_dist + 1:
                dist[next.x][next.y] = (cur_dist+1, cur_dir)
                current = [next] + current

maximaler_mehrwert = 0
beste_richtung = Direction.UP
target = None
for bonus in bonuses:
    # Schritt 1: Berechne entfernung
    d, direction = dist[bonus.position.x][bonus.position.y]
    # Schritt 2: Berechne "Mehrwert"
    wert = bonus.get_current_score() / d
    # Schritt 3: Falls ein neues maximum gefunden ist, wollen wir dorthin gehen
    if wert > maximaler_mehrwert:
        beste_richtung = direction
        target = bonus.position
        maximaler_mehrwert = wert


# bester_bonus ist jetzt somit unser Ziel
# Überprüfe nun für jede Richtung, ob ein Hindernis in diese Richtung ist
# und falls nicht, ob ein Schritt in diese Richtung die Entfernung zum Ziel verringert
# Falls beides erfüllt ist, wird die Richtung gewählt

# Oben als "Standartrichtung"
mySnake.direction = beste_richtung

