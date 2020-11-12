class Road():
    def __init__(self,node1,node2,button):
        self.button = button
        self.connectNodes = [node1,node2]
        self.player = None
        
    def getButton(self):
        return self.button
    def setPlayer(self,player):
        self.player = player
    def getPlayer(self):
        return self.player
    def getConnectNodes(self):
        return self.connectNodes
    
    
