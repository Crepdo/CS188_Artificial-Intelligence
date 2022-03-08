# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodlist = newFood.asList()
        ghostPoslist = [(ghost.getPosition()[0],ghost.getPosition()[1]) for ghost in newGhostStates]
        # fail:
        if min(newScaredTimes) <=0 and (newPos in ghostPoslist): return -1
        # get food:
        if newPos in currentGameState.getFood().asList(): return 1
        # sort 2 list to find closest
        closestFoodlist = sorted(newFoodlist,key=lambda x: util.manhattanDistance(x,newPos))
        closestGhostlist = sorted(ghostPoslist,key=lambda y: util.manhattanDistance(y,newPos))
        # 1/distance_food - 1/distance_ghost
        return (1/util.manhattanDistance(closestFoodlist[0],newPos)) - (1/util.manhattanDistance(closestGhostlist[0],newPos))

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        ghostNum = gameState.getNumAgents()-1
        
        # ghost,min:
        def minForcer(state, depth, ghostNo):
            # game end detection:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = 9e5
            for action in state.getLegalActions(ghostNo):
                if ghostNo == ghostNum: # last gost
                    value = min(value, maxForcer(state.getNextState(ghostNo, action), depth+1))
                else:
                    value = min(value, minForcer(state.getNextState(ghostNo, action), depth, ghostNo+1))
            return value

        # pacman,max:
        def maxForcer(state, depth):
            # game end detection:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = -9e5
            for action in state.getLegalActions(0):
                value = max(value, minForcer(state.getNextState(0,action), depth, 1))
            return value
        # init: start from pacman's actions:
        valuelist = [(action, minForcer(gameState.getNextState(0,action),0,1)) for action in gameState.getLegalActions(0)]
        # sort according to returned value (since start from MAX node):
        valuelist.sort(key=lambda k: k[1])
        #return the action
        return valuelist[-1][0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ghostNum = gameState.getNumAgents()-1
        
        # ghost,min:
        # pacmax: pacman's best option (max,downer limit) 
        # ghostmin: ghost's best option (min, upper limit)
        def minForcer(state, depth, ghostNo,pacmax,ghostmin):
            # game end detection:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = 9e10
            for action in state.getLegalActions(ghostNo):
                if ghostNo == ghostNum: # last gost
                    value = min(value, maxForcer(state.getNextState(ghostNo, action), depth+1, pacmax, ghostmin))
                else:
                    value = min(value, minForcer(state.getNextState(ghostNo, action), depth, ghostNo+1, pacmax, ghostmin))
                if value < pacmax: return value # pruning
                ghostmin = min(ghostmin, value)
            return value

        # pacman,max:
        def maxForcer(state, depth, pacmax, ghostmin):
            # game end detection:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = -9e10
            for action in state.getLegalActions(0):
                value = max(value, minForcer(state.getNextState(0,action), depth, 1, pacmax, ghostmin))
                if value > ghostmin: return value # pruning
                pacmax = max(pacmax, value)
            return value
    
        # init: start from pacman's actions, with pruning:
        pacmax = -9e5; ghostmin = 9e5
        path = None
        for action in gameState.getLegalActions(0):
            # for each ghost in the first layer, start from 1st ghost:
            it_val = minForcer(gameState.getNextState(0,action),0,1,pacmax, ghostmin)
            if it_val > ghostmin: return pacmax # pruning
            # max(), and choose the corresponding path
            if it_val > pacmax:
                pacmax = it_val
                path = action
        return path

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        ghostNum = gameState.getNumAgents()-1
        # ghost, exp:
        # no pruning
        def expForcer(state, depth, ghostNo):
            # game end detection:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = 0
            # probability:
            probability = 1/len(state.getLegalActions(ghostNo))
            for action in state.getLegalActions(ghostNo):
                if ghostNo == ghostNum: # last gost
                    value += probability*maxForcer(state.getNextState(ghostNo, action), depth+1)
                else:
                    value += probability*expForcer(state.getNextState(ghostNo, action), depth, ghostNo+1)
            return value

        # pacman,max:
        def maxForcer(state, depth):
            # game end detection:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            value = -9e10
            for action in state.getLegalActions(0):
                value = max(value, expForcer(state.getNextState(0,action), depth, 1))
            return value
    
        # init: start from pacman's actions:
        valuelist = [(action, expForcer(gameState.getNextState(0,action),0,1)) for action in gameState.getLegalActions(0)]
        # sort according to returned value (since start from MAX node):
        valuelist.sort(key=lambda k: k[1])
        #return the action
        return valuelist[-1][0]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()