from world import World

class Tournament:
    def __init__(self, players, group_size=4, sub=False):
        self.players = []
        self.group_size = group_size
        self.sub = sub
        self.ranked = False
        if len(players) > group_size:
            self.split = True
            self.left = Tournament(players[:int(len(players)/2)], group_size, True)
            self.right = Tournament(players[int(len(players)/2):], group_size, True)
        else:
            self.players = players
            self.split = False

    def play_tournament(self, screen, clock, width, height, size):
        while not self.play_last(screen,clock,width,height,size):
            pass
        self.players.sort(key=lambda p: p.score, reverse=True)
        return self.players[0].name

    def play_last(self, screen, clock, width, height, size):
        if self.split:
            if self.left.play_last(screen, clock, width, height, size) and self.right.play_last(screen ,clock, width, height, size):
                self.left.players.sort(key=lambda p: p.score, reverse=True)
                self.right.players.sort(key=lambda p: p.score, reverse=True)
                first_half = self.left.players[:int(self.group_size/2)]
                second_half = self.right.players[:int(self.group_size/2)]
                self.players =  first_half + second_half
                self.split = False
            return False
        else:
            if len(self.players) > int(self.group_size/2):
                world = World(self.players,width, height)
                world.simulate_and_show(screen,clock, size)
            return True




