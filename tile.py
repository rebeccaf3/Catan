class Tile():
    def __init__(self, resource, colour):
        self.resource = resource
        self.diceRoll = -1
        self.colour = colour
        
    def getType(self):
        return self.resource
    def setDiceRoll(self,roll):
        self.diceRoll = roll
    def getDiceRoll(self):
        return self.diceRoll
    
    def getColour(self):
        return self.colour
