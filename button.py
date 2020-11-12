import pygame
class Button():
    def __init__(self, colour, x,y,width,height):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = ""
        self.size = 60

    def setText(self,text):
        self.text = text
    def setColour(self,colour):
        self.colour = colour
        
    def changeSize(self,size):
        self.size = size

    def setWidthHeight(self,width,height):
        self.width = width
        self.height = height
        
    def draw(self,screen,outline):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        pygame.draw.rect(screen, self.colour, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.size)
            text = font.render(self.text, True, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
    
class CardButton(Button):
    def __init__(self,colour,x,y,height,width,card):
        Button.__init__(self,colour,x,y,height,width)
        self.cardType = card

    def getCardType(self):
        return self.cardType

class PlayerButton(Button):
    def __init__(self,colour,x,y,height,width,player):
        Button.__init__(self,colour,x,y,height,width)
        self.player = player
    def getPlayer(self):
        return self.player
