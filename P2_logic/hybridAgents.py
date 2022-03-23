# hybridAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import logic
import searchUtil
from game import Agent

class BaseAgent(Agent):
    def observationFunction(self, gameState):
        walls = gameState.getWalls()
        currentState = gameState.getPacmanPosition()
        ghosts = gameState.getGhostPositions()
        
#         ghosts = []
#         for agents in board.agentPositions[1:]:
#             ghosts.append(agents[1]) 

        
        # PKE meter is True if ghost is next door
        pkeMeter = False
        (x,y) = currentState
        if (x-1,y) in ghosts:
            pkeMeter = True
        elif (x+1,y) in ghosts:
            pkeMeter = True
        elif (x,y-1) in ghosts:
            pkeMeter = True
        elif (x,y+1) in ghosts:
            pkeMeter = True
        
        percept = {'pacman':currentState, 'pkeReading': pkeMeter, 'walls':walls}

        return percept


class HybridAgent(BaseAgent):
    
    def __init__(self):
        self.pkeReadings = {}
        self.safePositions = set()
        self.visited = set()
    
    def getAction(self, percept):
        currentPosition = percept['pacman']
        self.visited.add(currentPosition)
        
        # Current position is definitely safe
        self.safePositions.add(currentPosition)
        
        # Add PKE reading of current position
        self.pkeReadings[currentPosition] = percept['pkeReading']
        
#         # If no pke reading, add neighbors to safe list
#         if not percept['pkeReading']:
#             (x,y) = currentPosition
#             allNeighbors = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
#             for (nx,ny) in allNeighbors:
#                 if not percept['walls'][nx][ny]:
#                     self.safePositions.add((nx,ny))
        
#         # Go East
#         nextPosition = (currentPosition[0]+1,currentPosition[1])
#         nextSafe = isSafe(nextPosition, self.pkeReadings, self.safePositions, percept['walls'])
#         print "nextSafe={}".format(nextSafe)
        
        allSafeStatus =  findAllSafeStatus(self.pkeReadings, self.safePositions, percept['walls'])
        
        newSafePositions = []
        unsafePositions = []
        unsurePositions = []
        for ((x,y), status) in allSafeStatus.items():
            if status == True:
                self.safePositions.add((x,y))
            if (x,y) not in self.visited:
                if status == True:
                    newSafePositions.append((x,y))
                elif status == False:
                    unsafePositions.append((x,y))
                else:
                    unsurePositions.append((x,y))
                
        search = searchUtil.SafeSearchProblem()
        search.setWalls(percept['walls'])
        search.setStartState(currentPosition)
        search.setGoalStates(newSafePositions)
        search.setSafeStates(self.safePositions)
        plan = searchUtil.aStarSearch(search)

        if len(plan) > 0:
            action = plan[0]        
        else:
            search.setGoalStates(unsurePositions)
            search.setSafeStates(list(self.safePositions)+unsurePositions)
            plan = searchUtil.aStarSearch(search)

        if len(plan) > 0:
            action = plan[0]        
        else:
            action = None
        
        return action

def findAllSafeStatus(pkeReadings, knownSafePositions, walls):
    allSafePositions = {}
    for x in xrange(1,walls.width-1):
        for y in xrange(1,walls.height-1):
            if walls[x][y]:
                continue
            
            if (x,y) in knownSafePositions:
                allSafePositions[(x,y)] = True
            else:
                allSafePositions[(x,y)] = isSafe((x,y), pkeReadings, knownSafePositions, walls)

    return allSafePositions
    
def isSafe(position, pkeReadings, knownSafePositions, walls):
    exprList = []
    ghostStr = "G"
    pkeStr = "PKE"
    
    positionSymbol = logic.PropSymbolExpr(ghostStr,position[0],position[1])
    
    for (x,y) in knownSafePositions:
        exprList += [~logic.PropSymbolExpr(ghostStr,x,y)]

    for ((x,y), pkeReading) in pkeReadings.items():
        pkeSymbol = logic.PropSymbolExpr(pkeStr,x,y)
        if pkeReading:
            exprList += [pkeSymbol]
        else:
            exprList += [~pkeSymbol]
            
        allNeighbors = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        neighborSymbols = []
        for (nx,ny) in allNeighbors:
            if not walls[nx][ny]:
                neighborSymbols += [logic.PropSymbolExpr(ghostStr,nx,ny)]
        
        pkeExpr = pkeSymbol % reduce((lambda a,b: a|b), neighborSymbols)
        exprList += [logic.to_cnf(pkeExpr)]
        

#     # A pke reading in any square means that there is a ghost in at least one adjacent square
#     for x in xrange(1,walls.width-1):
#         for y in xrange(1,walls.height-1):
#             if walls[x][y]:
#                 continue
#                                
#             allNeighbors = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
#             neighborSymbols = []
#             for (nx,ny) in allNeighbors:
#                 if not walls[nx][ny]:
#                     neighborSymbols += [logic.PropSymbolExpr(ghostStr,nx,ny)]
#             
#             pkeSymbol = logic.PropSymbolExpr(pkeStr,x,y)            
#             pkeExpr = pkeSymbol % reduce((lambda a,b: a|b), neighborSymbols)
#             exprList += [logic.to_cnf(pkeExpr)]

    ghostModel = logic.pycoSAT(exprList + [positionSymbol])
#     print "ghostModel={}".format(ghostModel)
    if not ghostModel:
#         print "exprList={}".format(exprList + [positionSymbol])
        return True;
    else:
        noGhostModel = logic.pycoSAT(exprList + [~positionSymbol])
#         print "noGhostModel={}".format(noGhostModel)
        if not noGhostModel:
            return False;
        else:
            return None
    
    
