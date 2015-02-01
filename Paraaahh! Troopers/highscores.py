'''
High score class
'''
import os


class HighScores():

    def __init__(self):
        self.items = []
        self.load()

    def load(self):
        read_player = 1

        with open(os.path.join('data', 'highscores.dat'), 'r') as f:
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
        with open(os.path.join('data', 'highscores.dat'), 'w') as f:
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

    def display_high(self, scorefont, screen, p1_score):
        high = 0
        for i in self.items:
            if int(i.score) > high:
                high = int(i.score)
        if p1_score > 9999999:
            p1_score = 9999999
        player = scorefont.render('Score: %07d' % p1_score, True, (255, 255, 255))
        player_rect = player.get_rect()
        player_rect.topleft = (screen.get_width() / 1.7, screen.get_height() - 50)
        high_score = scorefont.render('High Score: %s' % high, True, (255, 255, 255))
        high_score_rect = high_score.get_rect()
        high_score_rect.topleft = (screen.get_width() / 24, screen.get_height() - 50)
        screen.blit(player, player_rect)
        screen.blit(high_score, high_score_rect)


class HighScoreEntry():

    def __init__(self, name, score):
        self.name = name
        self.score = score
