import random
class DevelopmentCards():
    def __init__(self):
        self.cardStack = ["knight","knight","knight","knight","knight","knight","knight","knight"
                    "victory point","victory point","victory point","victory point","victory point",
                    "monopoly",
                    "road building",
                    "year of plenty",]
        
    def shuffleCards(self):
        random.shuffle(self.cardStack)

##    def push(self,card):
##        self.cardStack.append(card)
        
    def pop(self):
        if len(self.cardStack) > 0:
            return (self.cardStack).pop(0)
        else:
            return -1
            
                
