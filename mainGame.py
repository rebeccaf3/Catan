LIGHTBLUE = (151,179,253) #start buttons
GREY = (169,169,169) #ore
SAND = (237,201,175) #desert
BROWN = (210,105,30) #wood
YELLOW = (255,255,0) #wheat
RED = (255, 0, 0) ##brick
GREEN = (0, 255, 0)  #sheep
PURPLE = (192, 15, 198) #player1
PINK = (255, 153, 234) #player2
BLUE = (0, 0, 255) #player3
ORANGE = (255,165,0) #player4
BLACK = (0, 0, 0) #outline
WHITE = (255, 255, 255) #background
numList = [11,12,9,4,6,5,10,3,11,4,8,8,10,9,3,5,2,6] #tile probabilities in order
RESOURCEOPTIONS = ["wood","wheat","brick","sheep","ore"]
RESOURCECOLOURS = [BROWN,YELLOW,RED,GREEN,GREY]

TILELINKS = ((0,3,4,7,8,12),(1,4,5,8,9,13),(2,5,6,9,10,14), #nodes that each tile is connected to
(7,11,12,16,17,22),(8,12,13,17,18,23),(9,13,14,18,19,24),(10,14,15,19,20,25),
(16,21,22,27,28,33),(17,22,23,28,29,34),(18,23,24,29,30,35),(19,24,25,30,31,36),(20,25,26,31,32,37),
(28,33,34,38,39,43),(29,34,35,39,40,44),(30,35,36,40,41,45),(31,36,37,41,42,46),
(39,43,44,47,48,51),(40,44,45,48,49,52),(41,45,46,49,50,53))

NODEADJACENCIES = ((3,4),(4,5),(5,6), #adjacency list of each node
(0,7),(0,1,8),(1,2,9),(2,10),
(3,11,12),(4,12,13),(5,13,14),(6,14,15),
(7,16),(7,8,17),(8,9,18),(9,10,19),(10,20),
(11,21,22),(12,22,23),(13,23,24),(14,24,25),(15,25,26),
(16,27),(16,17,28),(17,18,29),(18,19,30),(19,20,31),(20,32),
(21,33),(22,33,34),(23,34,35),(24,35,36),(25,36,37),(26,37),
(27,28,38),(28,29,39),(29,30,40),(30,31,41),(31,32,42),
(33,43),(34,43,44),(35,44,45),(36,45,46),(37,46),
(38,39,47),(39,40,48),(40,41,49),(41,42,50),
(43,51),(44,51,52),(45,52,53),(46,53),
(47,48),(48,49),(49,50))

NODEPOSITIONS = ((169, 41),(277, 41),(385, 41), #co-ordinates of each node
(117, 68),(222, 68),(330, 68),(437, 68),
(116, 132),(225, 132),(332, 132),(437, 132),
(63, 162),(166, 162),(278, 162),(384, 162),(491, 162),
(63, 225),(169, 225),(277, 225),(386, 225),(493, 225),
(10, 255),(115, 255),(223, 255),(328, 255),(438, 255),(546, 255),
(9, 316),(116, 316),(224, 316),(334, 316),(439, 316),(544, 316),
(61, 347),(168, 347),(274, 347),(384, 347),(490, 347),
(62, 411),(168, 411),(277, 411),(387, 411),(489, 411),
(118, 441),(224, 441),(330, 441),(437, 441),
(116, 502),(224, 502),(332, 502),(437, 502),
(168, 531),(278, 531),(384, 531))

import random
import math
import pygame

from tile import Tile
from button import Button, CardButton, PlayerButton
from node import Node
from board import Board
from player import Player
from road import Road
from developmentcard import DevelopmentCards

pygame.init()
screen = pygame.display.set_mode((820,600))
pygame.display.set_caption("Settlers of Catan")

def useDevelopmentCard(players,playerTurn,card,catanBoard,resources):
    msg = ""
    player = players[playerTurn]
    if card == "knight":
        playersToStealFromButtons = createPlayerButtons(players,playerTurn)
        if playersToStealFromButtons == []:
            msg = "No players to steal from"
        else:
            knightLoop = True
            while knightLoop:
                drawKnightScreen(playersToStealFromButtons)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = pygame.mouse.get_pos()
                        for b in playersToStealFromButtons:
                            if b.isOver(mousePos):
                                #steal resource
                                #remove development card if not cancelled
                                #add 1 to knight count
                                chosenPlayer = b.getPlayer()
                                stealResource = chosenPlayer.resources[random.randint(0,len(chosenPlayer.resources))-1]
                                player.giveResources([stealResource])
                                chosenPlayer.useResources([stealResource])
                                msg = [("You have stolen "+str(stealResource)),("from player "+str(chosenPlayer.ID+1))]
                                player.useCard("knight")
                                #print("Player",player.ID+1,"has used",player.knightCount,"knight(s)")
                                knightLoop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            knightLoop = False
                        
    elif card == "road building":
        #build two roads
        updateScreen(catanBoard, resources, player,msg)
        catanBoard, msg = buildRoad(catanBoard,player,None,"developmentCard0")
        
        if msg != "Building cancelled":
            updateScreen(catanBoard, resources, player,msg)
            catanBoard, msg = buildRoad(catanBoard,player,None,"developmentCard1")
            player.useCard("road building")
        msg = ""
        updateScreen(catanBoard, resources, player,msg)
        
        
    elif card == "year of plenty":
        errorMsg = ""
        x = 190
        y = 90
        rIncreaseButtons = []
        rDecreaseButtons = []
        plentyLoop = True
        for i in range(5):
            buttonI,buttonD = createResourceButtons(x,y,i)
            x+= 90    
            rIncreaseButtons.append(buttonI)
            rDecreaseButtons.append(buttonD)
        numResources = [0,0,0,0,0]
        while plentyLoop:
            drawYearOfPlentyScreen(rIncreaseButtons,rDecreaseButtons,numResources,errorMsg)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    for b in range(len(rIncreaseButtons)):
                        if rIncreaseButtons[b].isOver(mousePos):
                            numResources[b] += 1
                            #increase counter
                    for b in range(len(rDecreaseButtons)):
                        if rDecreaseButtons[b].isOver(mousePos):
                            if numResources[b] != 0:
                                numResources[b] -= 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        plentyLoop = False
                    elif event.key == pygame.K_RETURN:
                        #give player two resources only if they have selected 2
                        if sum(numResources) == 2:
                            #give player 2 resources
                            resourceLocs =  [i for i,val in enumerate(numResources) if val==1] #get the index of all 1s in numResources
                            if len(resourceLocs) == 0: #if no 1s, player has chosen 2 of the same resource
                                locationResource = numResources.index(2)
                                resourceLocs = [locationResource,locationResource]
                            resourcesToGive = []
                            for i in resourceLocs:
                                resourcesToGive.append(RESOURCEOPTIONS[i])
                            player.giveResources(resourcesToGive)
                            #print("Player",player.ID+1,"now has",player.resources)
                            player.useCard("year of plenty")
                            plentyLoop = False
                        else:
                            errorMsg = "Select only 2 resources"
                        
    elif card == "monopoly":
        #state one resource and all players give that resource to this player.
        resourceButtonsMonopoly = []
        x = 190
        y = 90
        for b in range(5):
            buttonR = Button(RESOURCECOLOURS[b],x,y,60,60)
            buttonR.setText(RESOURCEOPTIONS[b])
            buttonR.changeSize(20)
            x += 95
            resourceButtonsMonopoly.append(buttonR)
        monopolyLoop = True
        drawMonopolyScreen(resourceButtonsMonopoly)
        while monopolyLoop:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    for b in range(len(resourceButtonsMonopoly)):
                        if resourceButtonsMonopoly[b].isOver(mousePos):
                            msg = []
                            monopolyResource = RESOURCEOPTIONS[b]
                            for p in players:
                                if p != player:
                                    numResourcesMonopoly = p.countResource(monopolyResource)
                                    if numResourcesMonopoly != 0:
                                        resourceListM = [monopolyResource]*numResourcesMonopoly
                                        p.useResources(resourceListM)
                                        player.giveResources(resourceListM)
                                        addMsg = "Player "+str(p.ID+1)+" gives you: "+str(numResourcesMonopoly)+" "+monopolyResource
                                        msg.append(addMsg)
                                        
                            player.useCard("monopoly")
                            monopolyLoop = False
                            
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        monopolyLoop = False
        if msg == []: #if msg is [], a resource button was clicked on, but nobody had any resources to give
            msg = "Nobody had any "+monopolyResource
    return catanBoard, msg

def createDevelopmentCardButtons(player):
    playerCards = player.getDevelopmentCards()
    cardButtons = []
    x = 190
    y = 90
    duplicateCheckList = []
    for c in playerCards:
        if c not in duplicateCheckList:
            cButton = CardButton((165,207,250),x,y,85,60,c)
            x += 100
            cButton.setText(c)
            cButton.changeSize(20)
            cardButtons.append(cButton)
            duplicateCheckList.append(c)
    return cardButtons

def buyDevelopmentCard(player,allDevelopmentCards):
    if player.sufficientResources(["wheat","ore","sheep"]):
        collectCard = allDevelopmentCards.pop()
        if collectCard == -1:
            msg = "No more development cards"
        else:
            msg = ("Player "+str(player.ID+1)+" collects"," a "+collectCard)
            if collectCard == "victory point":
                player.alterVictoryPoints(1)
            else:
                player.collectDevelopmentCard(collectCard)
            player.useResources(["wheat","ore","sheep"])
    else:
        msg = ("Not enough resources")
    return msg

def developmentCardChoiceScreen(cardButtons):
    screen.fill(WHITE)
    for c in cardButtons:
        c.draw(screen,BLACK)
    pygame.display.flip()

    cardLoop = True
    while cardLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for c in cardButtons:
                    if c.isOver(mousePos):
                        return c.getCardType()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cardLoop = False
                    
def drawMonopolyScreen(resourceButtonsMonopoly):
    screen.fill(WHITE)
    writeText("Name one resource. All other players will give you all of the resources of that type that they own.",18,300,BLACK)
    for b in resourceButtonsMonopoly:
        b.draw(screen,BLACK)
    pygame.display.flip()
    
def drawYearOfPlentyScreen(rIncreaseButtons,rDecreaseButtons,numResources,errorMsg):
    screen.fill(WHITE)
    writeText("Choose 2 resources to collect",225,300,BLACK)
    if errorMsg != "":
        writeText(errorMsg,225,330,BLACK)
    for b in range(5):
        rIncreaseButtons[b].draw(screen,BLACK)
        rDecreaseButtons[b].draw(screen,BLACK)
    drawTradeNums(numResources,None)
    pygame.display.flip()

def drawKnightScreen(playersToStealFromButtons):
    screen.fill(WHITE)
    writeText("Choose a player to steal a card from",225,300,BLACK)
    for b in playersToStealFromButtons:
        b.draw(screen,WHITE)
    pygame.display.flip()


def handleLargestArmy(largestArmyPlayer,largestArmySize,player):
    msg = ""
    if (player.getKnightCount() > largestArmySize) and (player.getKnightCount() >= 3):
        largestArmySize = player.getKnightCount()
            
        if largestArmyPlayer != player: #a new/different player has got the largest army
            if largestArmyPlayer != None: #largest army has been taken from another player
                largestArmyPlayer.alterVictoryPoints(-2)
            player.alterVictoryPoints(2)
            msg = ["You have the largest army","Size: "+str(player.getKnightCount())+" knights","+2 victory points!"]
            largestArmyPlayer = player
    return largestArmyPlayer,largestArmySize,msg

def handleLongestRoad(longestRoadPlayer,longestRoadLen,catanBoard):
    msg = ""
    updatedLongestRoadPlayer, updatedLongestRoad = findLongestRoad(catanBoard)
    if (updatedLongestRoad >= 5) and (updatedLongestRoad > longestRoadLen): #if road longer than 5 (eligible for longest road points) and longest road achieved
        if updatedLongestRoadPlayer != longestRoadPlayer: #if longest road player has changed
            updatedLongestRoadPlayer.alterVictoryPoints(2)
            if longestRoadPlayer != None: #if longest road has been taken from another player
                longestRoadPlayer.alterVictoryPoints(-2)
            longestRoadPlayer = updatedLongestRoadPlayer
            longestRoadLen = updatedLongestRoad
            msg = ("Player "+str(longestRoadPlayer.ID+1)+" now has the","longest road of length "+str(longestRoadLen))
    return longestRoadPlayer, updatedLongestRoad, msg   

def findLongestRoad(catanBoard):
    longestRoadLen = 0
    longestRoadPlayer = None
    
    nodes = catanBoard.getNodes()
    existingNodes = []
    for n in nodes:
        if n.getStatus() != None:
            existingNodes.append(n)
    existingRoads = catanBoard.getRoads()
    visitedNodes = []
    
    for n in existingNodes:
        if n not in visitedNodes:
            player = n.getPlayer()
            searchList, visitedNodes = search(n,existingRoads,[],player,visitedNodes)
            #print(len(searchList),"player",searchList[0].getPlayer().ID+1)
            if len(searchList) > longestRoadLen:
                longestRoadLen = len(searchList)
                longestRoadPlayer = n.getPlayer()
    #print("LONGEST ROAD HELD BY",longestRoadPlayer.ID+1,"WITH LENGTH",longestRoadLen)
    return longestRoadPlayer,longestRoadLen
        
def search(startNode,existingRoads,searchList,player,visitedNodes):
    for r in existingRoads:
        if startNode in r.getConnectNodes():
            if (r not in searchList):
                for x in r.getConnectNodes():
                    if x != startNode:
                        rConnection = x
                if rConnection.getPlayer() == player:
                    visitedNodes.append(rConnection)
                if r.getPlayer() == player:
                    searchList.append(r)
                    searchList, visitedNodes = search(rConnection,existingRoads,searchList,player,visitedNodes)

    return searchList, visitedNodes
                    
def createPlayerButtons(players,playerTurn):
    x = 250
    y = 90
    playerButtons = []
    for player in players:
        if (player != players[playerTurn]) and (player.getResources() != []):
            buttonA = PlayerButton(player.getColour(),x,y,50,50,player)
            buttonA.setText(str(player.ID+1))
            x += 100
            playerButtons.append(buttonA)
    return playerButtons

def createResourceButtons(x,y,i):
    buttonI = Button(RESOURCECOLOURS[i%5],x,y,55,55)
    buttonD = Button(RESOURCECOLOURS[i%5],x,y+60,55,55)
    buttonI.setText(str(RESOURCEOPTIONS[i%5])+" +")
    buttonD.setText(str(RESOURCEOPTIONS[i%5])+" -")
    buttonI.changeSize(20)
    buttonD.changeSize(20)
    return buttonI, buttonD
        
def trade(players,playerTurn):
    #4 options below: other 3 players, "bank" as buttons, outline edge of chosen option
    #counter for each resource
    #if bank chosen, only 4 of 1 resource can be traded
    
    tradeButtons = createPlayerButtons(players,playerTurn)
    buttonA = PlayerButton(GREY,550,90,50,50,"BANK")
    buttonA.setText("B")
    tradeButtons.append(buttonA)

    errorMsg = ""
    x = 210
    y = 200
    numResources0 = [0,0,0,0,0]
    numResources1 = [0,0,0,0,0]

    resourceIncreaseButtons = []
    resourceDecreaseButtons = []
    for i in range(len(RESOURCEOPTIONS)*2):
        if i == 5:
            y += 180
            x = 210
        buttonI, buttonD = createResourceButtons(x,y,i)
        resourceIncreaseButtons.append(buttonI)
        resourceDecreaseButtons.append(buttonD)
        x+= 90
        
    tradePlayer = None
    chosenPlayerButton = None
    trading = True
    while trading:
        updateTradeScreen(numResources0,numResources1,tradeButtons,resourceIncreaseButtons,resourceDecreaseButtons,chosenPlayerButton,players[playerTurn],errorMsg)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for button in tradeButtons:
                    if button.isOver(mousePos):
                        chosenPlayerButton = button
                        pygame.display.flip()
                        tradePlayer = button.getPlayer()
                for buttonI in range(10):
                    if resourceIncreaseButtons[buttonI].isOver(mousePos):
                        if buttonI > 4:
                            numResources1[buttonI%5] += 1
                        else:
                            numResources0[buttonI%5] += 1
                        break
                for buttonD in range(10):
                    if resourceDecreaseButtons[buttonD].isOver(mousePos):
                        if buttonD > 4:
                            if numResources1[buttonD%5] != 0: #can't give negative amount of resources
                                numResources1[buttonD%5] -= 1
                        else:
                            if numResources0[buttonD%5] != 0:
                                numResources0[buttonD%5] -= 1
                        break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #check each player has sufficient resources to complete the trade
                    #if sufficient resources, make trade happen, then back to game
                    #if player is bank, check it is a 4 to 1 trade
                    #if insufficient resources print error message
                    player0Resources = []
                    player1Resources = []
                    for i in range(5):
                        for j in range(numResources0[i]):
                            player0Resources.append(RESOURCEOPTIONS[i])
                        for j in range(numResources1[i]):
                            player1Resources.append(RESOURCEOPTIONS[i])
                    if tradePlayer == "BANK":
                        if (players[playerTurn].sufficientResources(player0Resources)):
                            if (len(player0Resources) == 4) and (len(player1Resources) == 1): 
                                if player0Resources.count(player0Resources[0]) == 4:
                                    players[playerTurn].useResources(player0Resources)
                                    players[playerTurn].giveResources(player1Resources)
                                    trading = False
                                    break
                            errorMsg = "Must be a 4-1 trade with the bank"
                        else:
                            errorMsg = "Player has insufficient resources to complete this trade"
                    elif tradePlayer == None:
                        errorMsg = "Select a player to trade with"
                    else:
                        if (players[playerTurn].sufficientResources(player0Resources)) and (tradePlayer.sufficientResources(player1Resources)):
                            players[playerTurn].useResources(player0Resources) #take items off first player
                            tradePlayer.giveResources(player0Resources)        #give them to second player
                            tradePlayer.useResources(player1Resources)         #take items off second player
                            players[playerTurn].giveResources(player1Resources)#give them to first player
                            trading = False
                        else:
                            errorMsg = "Players have insufficient resources to complete this trade"
                elif event.key == pygame.K_ESCAPE:
                    trading = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

def drawTradeNums(numResources0,numResources1): #to draw only one row of numbers, give numResources1 = None
    x = 255
    y = 200
    for i in range(5):
        writeText(numResources0[i],x,y,BLACK)
        x += 90
    if numResources1 != None:
        y += 180
        x = 255
        for i in range(5):
            writeText(numResources1[i],x,y,BLACK)
            x+= 90

def drawTradeButtons(tradeButtons,resourceIncreaseButtons,resourceDecreaseButtons,chosenPlayerButton):
    for button in tradeButtons:
        if chosenPlayerButton == button:
            button.draw(screen,BLACK)
        else:
            button.draw(screen,WHITE)

    for i in range(len(resourceIncreaseButtons)):
        resourceIncreaseButtons[i].draw(screen,BLACK)
        resourceDecreaseButtons[i].draw(screen,BLACK)
    
def updateTradeScreen(numResources0,numResources1,tradeButtons,resourceIncreaseButtons,resourceDecreaseButtons,chosenPlayerButton,player,errorMsg):
    screen.fill(WHITE)
    writeText("Press 'Esc' to cancel trade",250,10,BLACK)
    drawTradeButtons(tradeButtons,resourceIncreaseButtons,resourceDecreaseButtons,chosenPlayerButton)
    drawTradeNums(numResources0,numResources1)
    writeText("Player "+str(player.ID+1)+" gives:",60,200,BLACK)

    textPlayer = outputResources(player)
    writeText(textPlayer,280,170,BLACK)

    if errorMsg != "":
        writeText(errorMsg,250,35,BLACK)
    
    if chosenPlayerButton != None: #a player to trade with has been chosen
        if chosenPlayerButton.getPlayer() == "BANK": #trading with the bank
            writeText("Bank gives:",60,380,BLACK)
        else: #trading with a player
            tradeText = outputResources(chosenPlayerButton.getPlayer())
            writeText(tradeText,280,350,BLACK)
            writeText("Player "+str(chosenPlayerButton.getPlayer().ID+1)+" gives:",60,380,BLACK)
        writeText("Press enter to confirm trade",250,550,BLACK)
    pygame.display.flip()

def updateScreen(catanBoard, resources, player, msg):
    nodes = catanBoard.getNodes()
    screen.fill(WHITE)

    #output player turn
    drawShape(750,50,30,4,0,player.getColour())
    writeText(player.ID + 1,746,45,WHITE)

    drawBoard(resources)
    drawNodes(nodes)
    drawRoads(catanBoard)
    
    rText = outputResources(player)
    writeText(rText,60,560,BLACK)
        
    #output last message onto screen
    y = 250
    if (type(msg) is tuple) or (type(msg) is list): #if a msg is a tuple/list, each element is on a new line
        for line in msg:
            writeText(line,580,y,BLACK)
            y += 20
    else:
        writeText(msg,580,y,BLACK)

    vText = "You have "+str(player.getVictoryPoints())+" victory point(s)"
    writeText(vText,570,560,BLACK)
    
    pygame.display.flip()

def drawRoads(catanBoard):
    roads = catanBoard.getRoads()
    for i in roads:
        (i.button).draw(screen,BLACK)

def drawBoard(resources):
    x = 170
    y = 100
    radius = 60

    indexTile = 0
    for i in range(3):
        drawShape((x+i*(radius * 1.8)),y, radius , 6 ,100,resources[indexTile].getColour())
        if resources[indexTile].getType() != "desert":
            drawNum((x+i*(radius * 1.8)),y,indexTile)
        indexTile += 1 

    x = x - (0.9 * radius)
    y = y + (1.55 * radius)

    for i in range(4):
        drawShape((x+i*(radius * 1.8)),y, radius , 6 ,100,resources[indexTile].getColour())
        if resources[indexTile].getType() != "desert":
            drawNum((x+i*(radius * 1.8)),y,indexTile)
        indexTile += 1 
        
    x = x - (0.9 * radius)
    y = y + (1.55 * radius)

    for i in range(5):
        drawShape((x + i*(radius * 1.8)), y, radius, 6, 100, resources[indexTile].getColour())
        if resources[indexTile].getType() != "desert":
            drawNum((x+i*(radius * 1.8)),y,indexTile)
        indexTile += 1  

    x = x + (0.9 * radius)
    y = y + (1.55 * radius)

    for i in range(4):
        drawShape((x+i*(radius * 1.8)),y, radius , 6 ,100,resources[indexTile].getColour())
        if resources[indexTile].getType() != "desert":
            drawNum((x+i*(radius * 1.8)),y,indexTile)
        indexTile += 1 

    x = x + (0.9 * radius)
    y = y + (1.55 * radius)

    for i in range(3):
        drawShape(x+i*(radius * 1.8),y, radius , 6 ,100,resources[indexTile].getColour())
        if resources[indexTile].getType() != "desert":
            drawNum((x+i*(radius * 1.8)),y,indexTile)
        indexTile += 1 
         
def drawNodes(nodes):
    for i in nodes:
        i.getButton().draw(screen,BLACK)
      
def drawShape(x,y,radius,numSides,rotation,colour):
    pts = []
    for i in range(6): #rotation = 100 other way
        newX = x + radius * math.cos(rotation + math.pi * 2 * i / numSides)
        newY = y + radius * math.sin(rotation + math.pi * 2 * i / numSides)
        pts.append([int(newX), int(newY)])
    pygame.draw.polygon(screen,colour,pts)
        
def drawNum(x,y,indexTile):
    font = pygame.font.SysFont(None,48)
    text = font.render(str(numList[indexTile]),True,BLACK)
    textrect = text.get_rect()
    textrect.centerx = x
    textrect.centery = y
    screen.blit(text, textrect)

def writeText(word,x,y,colour):
    font = pygame.font.SysFont('comicsans', 25)
    text = font.render(str(word), True, colour)
    return screen.blit(text,(x,y))
        
def setUpBoard():
    screen.fill(WHITE)           
    desert1 = Tile("desert",SAND)
    brick1 = Tile("brick",RED)
    brick2 = Tile("brick",RED)
    brick3 = Tile("brick",RED)
    ore1 = Tile("ore",GREY)
    ore2 = Tile("ore",GREY)
    ore3 = Tile("ore",GREY)
    wood1 = Tile("wood",BROWN)
    wood2 = Tile("wood",BROWN)
    wood3 = Tile("wood",BROWN)
    wood4 = Tile("wood",BROWN)
    sheep1 = Tile("sheep",GREEN)
    sheep2 = Tile("sheep",GREEN)
    sheep3 = Tile("sheep",GREEN)
    sheep4 = Tile("sheep",GREEN)
    wheat1 = Tile("wheat",YELLOW)
    wheat2 = Tile("wheat",YELLOW)
    wheat3 = Tile("wheat",YELLOW)
    wheat4 = Tile("wheat",YELLOW)
    resources = [desert1,brick1,brick2,brick3,ore1,ore2,ore3,wood1,wood2,wood3,wood4,sheep1,sheep2,sheep3,sheep4,wheat1,wheat2,wheat3,wheat4]
    random.shuffle(resources)

    for i in range(len(resources)):
        if resources[i].getType() != "desert":
            resources[i].setDiceRoll(numList[i])
        else:
            numList.insert(i,-1)
        
    catanBoard = Board()
    buttons = [Button(BLACK,NODEPOSITIONS[i][0],NODEPOSITIONS[i][1],10,10) for i in range(54)]
    nodes = [Node(i,buttons[i]) for i in range(54)]
    
    for t in range(len(TILELINKS)):
        for n in TILELINKS[t]:
            nodes[n].addTileLink(resources[t])
            
    for nodeInList in nodes:
        catanBoard.addNode(nodeInList)
    return resources, catanBoard

def buildSettlement(catanBoard,player,isStartTurns):
    nodes = catanBoard.getNodes()
    currentRoads = catanBoard.getRoads()
    validNodes = []
    
    for i in nodes:
        invalidNode = False
        if (i.getStatus() == None) and ((i.canBuild(currentRoads,player) == True) or (isStartTurns == True)):
            adjacentNodes = NODEADJACENCIES[i.getLocation()]
            for n in adjacentNodes:
                if nodes[n].getStatus() != None:
                    invalidNode = True
                    break
            if invalidNode == False:
                buttonA = i.getButton()
                validNodes.append(i)
                buttonA.draw(screen,WHITE)
                
    pygame.display.flip()
    
    if validNodes == []:
       return catanBoard, None, "Nowhere to build"
    pygame.draw.rect(screen, WHITE, (570,240,220,300))
    writeText("Build a settlement",600,250,BLACK)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            mousePos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in validNodes:
                    if (i.getButton()).isOver(mousePos):
                        if not isStartTurns:
                            player.useResources(["wood","brick","wheat","sheep"])
                        (i.getButton()).setColour(player.getColour())
                        i.setStatus("settlement")
                        i.setPlayer(player)
                        player.alterVictoryPoints(1)
                        catanBoard.alterNode(i,i.getLocation())
                        return catanBoard,i, ""
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE) and (isStartTurns == False):
                    return catanBoard, None, ""
            elif event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

def buildCity(catanBoard,player):
    nodes = catanBoard.getNodes()
    canUpgradeNodes = []
    for n in nodes:
        if (n.getStatus() == "settlement") and (n.getPlayer() == player):
            canUpgradeNodes.append(n)
            n.getButton().draw(screen,WHITE)
    if canUpgradeNodes == []:
        return catanBoard, "Nowhere to build"
    
    pygame.draw.rect(screen, WHITE, (570,240,220,300))
    writeText("Build a city",600,250,BLACK)
    pygame.display.flip()
    
    cityLoop = True
    pygame.display.flip()
    while cityLoop:
        for event in pygame.event.get():
            mousePos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for c in canUpgradeNodes:
                    if (c.getButton()).isOver(mousePos):
                        (c.getButton()).setWidthHeight(20,20)
                        c.setStatus("city")
                        pygame.display.flip()
                        player.alterVictoryPoints(1)
                        catanBoard.alterNode(c,c.getLocation())
                        player.useResources(["wheat","wheat","ore","ore","ore"])
                        cityLoop = False                    
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    cityLoop = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
    return catanBoard, ""

def buildRoad(catanBoard,player,nodeConnect,mode): #to test for valid nodes, give nodeConnect = None. if not, give an object of the only valid node #mode = startTurns,developmentCard0,developmentCard1,regular
    nodes = catanBoard.getNodes()
    currentRoads = catanBoard.getRoads()
    if nodeConnect != None:
        validNodes = [nodeConnect]
    else:
        validNodes = []
        for checkRoad in currentRoads:
            if checkRoad.getPlayer() == player:
                for connection in checkRoad.getConnectNodes():
                    validNodes.append(connection)
        
    roadOptions = []
    roadBuilt = False
                
    currentNodePairs = []
    for i in currentRoads:
        currentNodePairs.append([i.getConnectNodes()[0].getLocation(),i.getConnectNodes()[1].getLocation()]) #the location of the 2 nodes that roads connect to
        
    for n in validNodes:
        adjacentNodes = list(NODEADJACENCIES[n.getLocation()])
        adjacentNodesCopy = list(adjacentNodes)
        for checkNode in adjacentNodesCopy: #make sure they dont overwrite existing roads
            if ([n.getLocation(),checkNode] in currentNodePairs) or ([checkNode,n.getLocation()] in currentNodePairs):
                adjacentNodes.remove(checkNode)

        adjacentNodeCoordinates = [(NODEPOSITIONS[adjacentNode]) for adjacentNode in adjacentNodes]
        nodeCoordinates = (NODEPOSITIONS[n.getLocation()])
        coordinates = []
        for i in adjacentNodeCoordinates: #loop through adjacent coordinates to work out the coordinates to place each road at
            appendCoordinate = ((i[0] + nodeCoordinates[0])//2,(i[1] + nodeCoordinates[1])//2)
            coordinates.append(appendCoordinate)

        tempButtons = [(Button(WHITE,i[0],i[1],15,5)) for i in coordinates]
        tempRoads = [(Road(n,nodes[adjacentNodes[roadIndex]],tempButtons[roadIndex])) for roadIndex in range(len(coordinates))] #all temp roads for 1 node
        
        for i in tempRoads:
            roadOptions.append(i)

    if len(roadOptions) == 0:
        return catanBoard, "Nowhere to build"

    pygame.draw.rect(screen, WHITE, (570,240,220,300))
    writeText("Build a road",600,250,BLACK)

    for option in roadOptions:
        tempRoadButton = option.getButton()
        tempRoadButton.draw(screen,BLACK)
    pygame.display.flip()
    
    while roadBuilt == False:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for road in roadOptions:
                    if (road.getButton()).isOver(mousePos): #change player, add to catanboard change colour
                        if mode == "regular":
                            player.useResources(["wood","brick"])
                        road.setPlayer(player)
                        (road.getButton()).setColour(player.getColour())
                        catanBoard.addRoad(road)
                        roadBuilt = True
                        break
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE) and (mode != "startTurns") and (mode != "developmentCard1"):
                    if (mode == "developmentCard0"):
                        return catanBoard,"Building cancelled"
                    return catanBoard, ""
            elif event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
    return catanBoard, ""

def createPlayers():
    player1 = Player(0,PURPLE)
    player2 = Player(1,PINK)
    player3 = Player(2,BLUE)
    player4 = Player(3,ORANGE)
    return [player1,player2,player3,player4]

def startTurns(catanBoard,players,playerTurn,resources):
    #going backwards through players
    #build one settlement and one road (road has to connect to settlement)
    #collect resources based off where the settlement is
    #go forwards through players, repeat but do not collect resources this time

    for i in range(8):        
        catanBoard, settlementNode = buildSettlement(catanBoard,players[playerTurn],True)[0:2]
        if i <= 3: #collect resources
            tilesResources = settlementNode.tileLinks
            for t in tilesResources:
                if t.resource != "desert": #dont let them collect a desert
                    (players[playerTurn]).giveResources([t.resource])
        updateScreen(catanBoard,resources,players[playerTurn],"")
            
        catanBoard = buildRoad(catanBoard,players[playerTurn],settlementNode,"startTurns")[0]
        
        
        if i <= 2:
            playerTurn = (playerTurn - 1) % 4
        elif (i != 7) and (i != 3):
            playerTurn = (playerTurn + 1) % 4
        
        updateScreen(catanBoard,resources,players[playerTurn],"")
    
    return playerTurn, catanBoard

def rollDie():
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    return (dice1+dice2)

def distributeResources(roll,catanBoard,resources):
    nodes = catanBoard.getNodes()
    for n in nodes:
        tiles = n.tileLinks
        for t in tiles:
            if (t.getDiceRoll() == roll):
                if n.status == "settlement":
                    player = n.getPlayer()
                    player.giveResources([t.resource])
                    #print("Player",player.ID + 1,"gets",t.resource)
                elif n.status == "city":
                    player = n.getPlayer()
                    player.giveResources([t.resource]*2)
                    #print("Player",player.ID+1,"gets 2",t.resource)

def outputResources(player):
    resourceCounts = []
    for rType in RESOURCEOPTIONS:    
        rCount = player.countResource(rType)
        if rCount != 0:
            resourceCounts.append(((rCount),(rType)))

    if len(resourceCounts) != 0:
        text = str("Player "+str(player.ID+1)+" has: ")
        for r in range(len(resourceCounts)):
            if r != (len(resourceCounts)-1):
                text = text+(str((resourceCounts[r])[0])+" "+(resourceCounts[r])[1]+", ")
            else:
                text = text+(str((resourceCounts[r])[0])+" "+(resourceCounts[r])[1])
    else:
        text = ("Player "+str(player.ID+1)+" has no resources")
    return text

def checkVictory(players):
    for p in players:
        if p.getVictoryPoints() >= 10:
            return p


def drawHomeScreen(startButton,instructionsButton):
    screen.fill(WHITE)
    startButton.draw(screen,BLACK)
    instructionsButton.draw(screen,BLACK)
    pygame.display.flip()
    
def homeScreen():
    startButton = Button(LIGHTBLUE, 260,100,340,50)
    startButton.setText("PLAY CATAN")
    instructionsButton = Button(LIGHTBLUE,260,200,340,50)
    instructionsButton.setText("INSTRUCTIONS")
    
    drawHomeScreen(startButton,instructionsButton)
    homeScreenLoop = True
    while homeScreenLoop:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if startButton.isOver(mousePos):
                    return
                elif instructionsButton.isOver(mousePos):
                    showInstructions()
                    drawHomeScreen(startButton,instructionsButton)
            elif event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
                
def showInstructions():
    screen.fill(WHITE)
    writeText("INSTRUCTIONS:",100,50,BLACK)
    writeText("i = display instructions",100,100,BLACK)
    writeText("s = build settlement",100,150,BLACK)
    writeText("r = build road",100,200,BLACK)
    writeText("d = roll dice",100,250,BLACK)
    writeText("t = trade",100,300,BLACK)
    writeText("b = buy development card",100,350,BLACK)
    writeText("c = build city",100,400,BLACK)
    writeText("u = use development card",100,450,BLACK)
    writeText("right arrow = next player turn",100,500,BLACK)
    writeText("esc = cancel action",100,550,BLACK)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN):
                return
            
def main():
    homeScreen()
    largestArmyPlayer = None
    largestArmySize = 0
    longestRoadPlayer = None
    longestRoadLen = 0
    victoryPlayer = None
    game = True
    msg = ("Press d to","roll the dice")
    
    clock = pygame.time.Clock()
    allDevelopmentCards = DevelopmentCards()
    allDevelopmentCards.shuffleCards()
    players = createPlayers()
    resources, catanBoard = setUpBoard()
    playerTurn = random.randint(0,3)
    updateScreen(catanBoard, resources, players[playerTurn],msg)
    playerTurn, catanBoard = startTurns(catanBoard,players,playerTurn,resources)
    updateScreen(catanBoard, resources, players[playerTurn],msg)
   

    diceRolled = False
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if players[playerTurn].sufficientResources(["wood","brick","sheep","wheat"]):
                        catanBoard, msg = buildSettlement(catanBoard,players[playerTurn],False)[::2]
                        victoryPlayer = checkVictory(players)
                    else:
                        msg = ("Not enough resources")
                    updateScreen(catanBoard, resources,players[playerTurn],msg)
                elif event.key == pygame.K_d:
                    if diceRolled == False:
                        roll = rollDie()
                        msg = ("You roll a "+str(roll))
                        distributeResources(roll,catanBoard,resources)
                        diceRolled = True
                    else:
                        msg = "Already rolled"
                    updateScreen(catanBoard, resources,players[playerTurn],msg)
                elif event.key == pygame.K_RIGHT:
                    if diceRolled == True:
                        playerTurn = (playerTurn + 1) % 4
                        msg = ("Press d to","roll the dice")
                        diceRolled = False
                    else:
                        msg = ("Roll dice before","finishing your turn!")
                    updateScreen(catanBoard, resources, players[playerTurn],msg)
                    
                elif event.key == pygame.K_r:
                    if players[playerTurn].sufficientResources(["wood","brick"]):
                        catanBoard, msg = buildRoad(catanBoard,players[playerTurn],None,"regular")
                        if msg == "":
                            longestRoadPlayer, longestRoadLen, msg = handleLongestRoad(longestRoadPlayer,longestRoadLen,catanBoard)
                            victoryPlayer = checkVictory(players)
                    else:
                        msg = "Not enough resources"
                    updateScreen(catanBoard, resources,players[playerTurn],msg)
                    
                elif event.key == pygame.K_t:
                    if players[playerTurn].getResources() != []:
                        trade(players,playerTurn)
                        msg = ""
                    else:
                        msg = ("You have no resources","to trade") 
                    updateScreen(catanBoard, resources,players[playerTurn],msg)
                    
                elif event.key == pygame.K_b:
                    msg = buyDevelopmentCard(players[playerTurn],allDevelopmentCards)
                    victoryPlayer = checkVictory(players)
                    updateScreen(catanBoard, resources,players[playerTurn],msg)
                elif event.key == pygame.K_c:
                    if players[playerTurn].sufficientResources(["wheat","wheat","ore","ore","ore"]):
                        catanBoard,msg = buildCity(catanBoard,players[playerTurn])
                        victoryPlayer = checkVictory(players)
                    else:
                        msg = ("Not enough resources")
                    updateScreen(catanBoard, resources,players[playerTurn],msg)
                elif event.key == pygame.K_i:
                    showInstructions()
                    updateScreen(catanBoard, resources,players[playerTurn],"")

                ############################TESTING BUTTONS#######################################################        
                elif event.key == pygame.K_9:
                    players[playerTurn].collectDevelopmentCard("knight")
                    players[playerTurn].collectDevelopmentCard("monopoly")
                    players[playerTurn].collectDevelopmentCard("road building")
                    players[playerTurn].collectDevelopmentCard("year of plenty")
                elif event.key == pygame.K_8:
                    players[playerTurn].giveResources(["wood","wheat","brick","sheep","ore"])
                    #players[playerTurn].giveResources(["wood","wheat","brick","sheep","ore"])
                    updateScreen(catanBoard, resources, players[playerTurn],msg)
                elif event.key == pygame.K_7:
                    players[playerTurn].alterVictoryPoints(1)
                    victoryPlayer = checkVictory(players)
                    updateScreen(catanBoard, resources, players[playerTurn],msg)
                ##################################################################################################
                    
                elif event.key == pygame.K_u:
                    #check player has development card
                    #if they do go to chose development card screen
                    cardButtons = createDevelopmentCardButtons(players[playerTurn])
                    if len(cardButtons) != 0:
                        card = developmentCardChoiceScreen(cardButtons)
                        if card != None:
                            catanBoard,msg = useDevelopmentCard(players,playerTurn,card,catanBoard,resources)
                            if card == "road building":
                                longestRoadPlayer, longestRoadLen, msg = handleLongestRoad(longestRoadPlayer,longestRoadLen,catanBoard)
                                victoryPlayer = checkVictory(players)
                            elif card == "knight":
                                largestArmyPlayer,largestArmySize,newMsg = handleLargestArmy(largestArmyPlayer,largestArmySize,players[playerTurn])
                                if newMsg != "":
                                    msg.append("")
                                    for line in newMsg:
                                        msg.append(line)
                                victoryPlayer = checkVictory(players)
                    else:
                        msg = ("You have not got","any development cards")
                    updateScreen(catanBoard, resources, players[playerTurn],msg)
                    
                if victoryPlayer != None:
                    msg = ("Player "+str(victoryPlayer.ID+1)+" wins!")
                    updateScreen(catanBoard, resources, players[playerTurn],msg)
                    replayButton = Button(LIGHTBLUE,600,300,150,50)
                    replayButton.setText("Replay")
                    quitButton = Button(LIGHTBLUE,600,380,150,50)
                    quitButton.setText("Quit")
                    replayButton.draw(screen,BLACK)
                    quitButton.draw(screen,BLACK)
                    pygame.display.flip()
                    victoryScreen(replayButton,quitButton)
                    
        clock.tick(60)

def victoryScreen(replayButton,quitButton):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if replayButton.isOver(mousePos):
                    numList.remove(-1)
                    main()
                elif quitButton.isOver(mousePos):
                    pygame.quit()
                    raise SystemExit

main()
