class Player():
    def __init__(self, ID, colour):
        self.ID = ID
        self.colour = colour
        self.victoryPoints = 0
        self.resources = []
        self.developmentCards = []
        self.knightCount = 0
    def getResources(self):
        return self.resources
    def getKnightCount(self):
        return self.knightCount
    def getVictoryPoints(self):
        return self.victoryPoints
    def useCard(self,card):
        if card == "knight":
            self.knightCount += 1
        self.developmentCards.remove(card)
    def collectDevelopmentCard(self,card):
        self.developmentCards.append(card)
    def getDevelopmentCards(self):
        return self.developmentCards
    def getColour(self):
        return self.colour

    def alterVictoryPoints(self,num):
        self.victoryPoints += num

    def giveResources(self,resources):
        for r in resources:
            (self.resources).append(r)
    def useResources(self,resources):
        for r in resources:
            (self.resources).remove(r)
    
    def countResource(self,resource):
        count = 0
        for r in self.resources:
            if r == resource:
                count += 1
        return count
    def sufficientResources(self,cost): #will return a bool
        resourcesTemp = self.resources.copy()
        try:
            for item in cost:
                resourcesTemp.remove(item)
            return True
        except:
            return False
