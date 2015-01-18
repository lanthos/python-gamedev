'''
High score class
'''


class HighScores():

    def __init__(self):
        self.items = []
        self.load()

    def load(self):
        read_player = 1

        with open('highscores.dat', 'r') as f:
            content = f.read()
            player = ""
            score = ""

            for i in range(0, len(content)):
                if content[i] == '\n':
                    if read_player:
                        read_player = 0
                    else:
                        self.add(HighScoreEntry(player, score))
                        read_player = 1
                        player = ""
                        score = ""
                else:
                    if read_player:
                        player += content[i]
                    else:
                        score += content[i]

    def save(self):
        res = ""
        for item in self.items:
            res += item.name + "\n" + item.score + "\n"
        with open('highscores.dat', 'w') as f:
            f.write(res)

    def add(self, item):
        newl = []
        inserted = 0
        if len(self.items) == 0:
            self.items = [item]
            return
        for i in self.items:
            if int(item.score) < int(i.score):
                newl.append(i)
            else:
                if not inserted:
                    newl.append(item)
                    inserted = 1
                newl.append(i)
        if not inserted:
            newl.append(item)
        self.items = newl


class HighScoreEntry():

    def __init__(self, name, score):
        self.name = name
        self.score = score
