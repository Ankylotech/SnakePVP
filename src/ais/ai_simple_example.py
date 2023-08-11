#bot
# ^ So muss jede Datei starten

# Ziel des Bots:
# Berechne für jedes Collectable den Score pro verwendeter Zeit um dorthin zu gelangen (Angenähert mit Manhatten-Distanz)
# und gehe zu dem mit dem größten "Mehrwert"

position = mySnake.head()
maximaler_mehrwert = 0
bester_bonus = None
for bonus in bonuses:
    # Schritt 1: Berechne entfernung
    dist = bonus.position.dist(position)
    # Schritt 2: Berechne "Mehrwert"
    wert = bonus.get_current_score() / dist
    # Schritt 3: Falls ein neues maximum gefunden ist, wollen wir dorthin gehen
    if wert > maximaler_mehrwert:
        bester_bonus = bonus.position
        maximaler_mehrwert = wert


# bester_bonus ist jetzt somit unser Ziel
# Überprüfe nun für jede Richtung, ob ein Hindernis in diese Richtung ist
# und falls nicht, ob ein Schritt in diese Richtung die Entfernung zum Ziel verringert
# Falls beides erfüllt ist, wird die Richtung gewählt

# Oben als "Standartrichtung"
richtung = Direction.UP
# Entfernung ist maximal
entfernung = world.width * world.height
# Ein Schritt nach oben
schritt = world.move_and_teleport(position, Direction.UP)
# Falls nach oben kein Hindernis kommt, wird die Entfernung verbessert
if not world.obstacle(schritt):
    entfernung = schritt.dist(bester_bonus)

# Schritt nach unten
schritt = world.move_and_teleport(position, Direction.DOWN)
# Falls nach unten kein Hindernis kommt und die Entfernung kleiner wird, wird die Richtung und die Entfernung verbessert
if not world.obstacle(schritt) and entfernung > schritt.dist(bester_bonus):
    entfernung = schritt.dist(bester_bonus)
    richtung = Direction.DOWN

# Schritt nach links
schritt = world.move_and_teleport(position, Direction.LEFT)
# Falls nach links kein Hindernis kommt und die Entfernung kleiner wird, wird die Richtung und die Entfernung verbessert
if not world.obstacle(schritt) and entfernung > schritt.dist(bester_bonus):
    entfernung = schritt.dist(bester_bonus)
    richtung = Direction.LEFT

# Schritt nach rechts
schritt = world.move_and_teleport(position, Direction.RIGHT)
# Falls kein Hindernis kommt und die Entfernung kleiner wird, wird die Richtung und die Entfernung verbessert
if not world.obstacle(schritt) and entfernung > schritt.dist(bester_bonus):
    entfernung = schritt.dist(bester_bonus)
    richtung = Direction.RIGHT

mySnake.direction = richtung

