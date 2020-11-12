class Node():
    def __init__(self,location,button):
        self.location = location # 0,1,2,3,
        self.tileLinks = [] #ids of linked tiles (what resources this node will give)
        self.status = None #None, settlement, city
        self.button = button
        self.player = None

    def setPlayer(self,player):
        self.player = player
    def getPlayer(self):
        
        return self.player
    def setStatus(self,status):
        self.status = status
    def getStatus(self):
        return self.status

    def getButton(self):
        return self.button
    def getLocation(self):
        return self.location
    def addTileLink(self,link):
        (self.tileLinks).append(link)
    def canBuild(self,currentRoads,player):
        for road in currentRoads:
            if road.getPlayer() == player:
                for node in road.getConnectNodes():
                    if node.getLocation() == self.location:
                        return True
        return False  
    
