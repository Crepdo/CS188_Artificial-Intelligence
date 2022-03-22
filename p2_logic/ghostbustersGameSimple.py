# ghostbustersGameSimple.py
# -------------------------
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


import sys
import layout
import logicAgents
import hybridAgents
import warnings
from game import Actions
from game import Directions

class GhostbustersGameSimple:
    def __init__(self, layoutName):
        board = layout.getLayout(layoutName)
        self.walls = board.walls
        self.boardText = board.layoutText
        for i in xrange(len(self.boardText)):
            self.boardText[i] = list(self.boardText[i])

        self.goal = None
        for x in xrange(board.food.width):
            for y in xrange(board.food.height):
                if board.food[x][y]:
                    self.goal = (x,y)
                    
        self.currentState = board.agentPositions[0][1]
        self._agentAlive = True
        
        self.ghosts = []
        for agents in board.agentPositions[1:]:
            self.ghosts.append(agents[1]) 

    def getStartState(self):
        return self.currentState
               
    def getActions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """
        actions = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                actions.append(action)

        return actions
    
    def getResult(self, state, action):
        """
        Given a state and an action, returns resulting state and a cost of 1, which is
        the incremental cost of expanding to that successor.
        Returns (next_state, cost)
        """
        x,y = state
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        if (not self.walls[nextx][nexty]) and (not self.walls[nextx][nexty]):
            nextState = (nextx, nexty)
            cost = 1
            return (nextState, cost)
        else:
            warnings.warn("Warning: checking the result of an invalid state, action pair.")
            return (state,0)
        
    def goalTest(self, state):
        goal = (state == self.goal)
        if not goal:
            for ghost in self.ghosts:
                if state == ghost:
                    goal = True
                    break
                
        return goal

    def currentPercept(self):
        # PKE meter is True if ghost is next door
        pkeMeter = False
        (x,y) = self.currentState
        if (x-1,y) in self.ghosts:
            pkeMeter = True
        elif (x+1,y) in self.ghosts:
            pkeMeter = True
        elif (x,y-1) in self.ghosts:
            pkeMeter = True
        elif (x,y+1) in self.ghosts:
            pkeMeter = True
        
        percept = {'pacman':self.currentState, 'pkeReading': pkeMeter, 'walls':self.walls}

        return percept

    def _updateBoardText(self):
        height = len(self.boardText) # Board y coordinate is inverted
        
        # Clear old pacman and ghosts
        for i in xrange(len(self.boardText)):
            row = self.boardText[i]
            for j in xrange(len(row)):
                if row[j] == 'P' or row[j] == 'G':
                    self.boardText[i][j] = ' '
                    
        # Set current ghosts
        for ghost in self.ghosts:
            self.boardText[height-1-ghost[1]][ghost[0]] = 'G'                
                    
        # Set current pacman
        if self.boardText[height-1-self.currentState[1]][self.currentState[0]] == 'G':
            self.boardText[height-1-self.currentState[1]][self.currentState[0]] = 'X'
        else:
            self.boardText[height-1-self.currentState[1]][self.currentState[0]] = 'P'

    def printBoard(self):
        for rowText in self.boardText:
            print (''.join(rowText))

    def run(self, agent):
        print ("Initial board")
        self.printBoard()
        while self._agentAlive:
            if self.goalTest(self.currentState):
                "Pacman wins!"
                break;
                
            percept = self.currentPercept()
            print ("percept={}".format(percept))
            action = agent.getAction(percept)
            if action == None:
                warnings.warn("Warning invalid action returned by agent: "+str(action))
                break
            (nextState, _) = self.getResult(self.currentState, action)
            self.currentState = nextState
            self._updateBoardText()
            
            print ()
            print (action)
            self.printBoard()
            
        
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        layoutName = sys.argv[1]
    else:
        layoutName = "line"
    
    game = GhostbustersGameSimple(layoutName)
    
    agent = hybridAgents.HybridAgent(game)
    game.run(agent)
