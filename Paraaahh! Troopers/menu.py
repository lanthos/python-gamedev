'''
Menu Class!  Soo pretty...
'''


class Menu():
    def __init__(self):
        self.sub_menu = None
        self.items = []
        self.selected = None
        
    def add_item(self, item):																								
        self.items.append(item)
        
    def move_down(self):
        if self.selected == None:
            self.selected = -1
        
        if self.selected < len(self.items) - 1:
            self.selected += 1
        else:
            self.selected = 0
        if self.items[self.selected].selectable == 0:
            self.move_down()
        
    def move_up(self):
        if self.selected == None:
            self.selected = len(self.items)
            
        if self.selected > 0:
            self.selected -= 1
        else:
            self.selected = len(self.items) - 1
        
        if self.items[self.selected].selectable == 0:
            self.move_up()
    
    def clear(self):
        del self.items
        self.items = []
    
    def mainmenu(self):
        self.clear()
        self.add_item(MenuItem("New Game", "newgame"))
        # self.add_item(MenuItem("Options", "options"))
        self.add_item(MenuItem("Highscores", "scores"))
        self.add_item(MenuItem("Credits", "credits"))
        self.add_item(MenuItem("Quit", "quit"))
        self.add_item(MenuItem("Use keyboard to play", "pause"))
        self.selected = None
        self.move_down()
        
    def ingamemenu(self):
        self.clear()
        self.add_item(MenuItem("PAUSE MENU", "pause"))
        self.add_item(MenuItem("Return", "returntogame"))
        self.add_item(MenuItem("New Game", "newgame"))
        # self.add_item(MenuItem("Options", "options"))
        self.add_item(MenuItem("Highscores", "scores"))
        self.add_item(MenuItem("Credits", "credits"))
        self.add_item(MenuItem("Quit", "quit"))
        self.selected = None	
        self.move_down()
        
    def creditsmenu(self):
        self.clear()
        self.add_item(MenuItem("Programming", ""))
        newm = MenuItem("Jeremy Kenyon", "")
        newm.align = "right"
        self.add_item(newm)
        self.add_item(MenuItem("Graphics", ""))
        newm = MenuItem("Jeremy Kenyon", "")
        newm.align = "right"
        self.add_item(newm)
        self.add_item(MenuItem("Testing", ""))
        newm = MenuItem("Jeremy Kenyon", "")
        newm.align = "right"
        self.add_item(newm)
        self.add_item(MenuItem("Back", "mainmenu"))
        self.selected = None
        self.move_down()
        
    def highscoresmenu(self, highscores):
        self.clear()
        c = 0
        for score in highscores.items:
            if c < 4:
                self.add_item(MenuItem(score.name, ""))
                newm = MenuItem(score.score, "")
                newm.align = "right"
                self.add_item(newm)
            c += 1
        self.add_item(MenuItem("Back", "mainmenu"))
        self.selected = None
        
    
class MenuItem():
    """Menu items"""
    def __init__(self, caption, changestate):
        self.caption = caption
        if changestate == "":
            self.selectable = 0
            self.align = "left"
        elif changestate == 'pause':
            self.selectable = 0
            self.align = "center"
        else:
            self.selectable = 1
            self.align = "center"
            self.changestate = changestate