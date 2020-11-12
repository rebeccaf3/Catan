class Board():
    def __init__(self):
        self.nodes = [] #a list of node objects
        self.roads = []
    def addNode(self,node):
        (self.nodes).append(node)
    def addRoad(self,road):
        (self.roads).append(road)
    def getNodes(self):
        return self.nodes
    def getRoads(self):
        return self.roads
    def alterNode(self,node,index):
        self.nodes[index] = node
