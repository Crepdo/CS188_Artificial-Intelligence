# logicAgents.py
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


"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a LogicAgent that uses
logicPlan.positionLogicPlan, run the following command:

> python pacman.py -p LogicAgent -a fn=positionLogicPlan

Commands to invoke other planning methods can be found in the project
description.

You should NOT change code in this file

Good luck and happy planning!
"""

from game import Directions
from game import Agent
from game import Actions
import util
import time
import warnings
import logicPlan

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of logicPlan.py          #
#######################################################

class LogicAgent(Agent):
    """
    This very general logic agent finds a path using a supplied planning
    algorithm for a supplied planning problem, then returns actions to follow that
    path.

    As a default, this agent runs positionLogicPlan on a
    PositionPlanningProblem to find location (1,1)

    Options for fn include:
      positionLogicPlan or plp
      foodLogicPlan or flp
      foodGhostLogicPlan or fglp


    Note: You should NOT change any code in LogicAgent
    """

    def __init__(self, fn='positionLogicPlan', prob='PositionPlanningProblem', plan_mod=logicPlan):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the planning function from the name and heuristic
        if fn not in dir(plan_mod):
            raise AttributeError (fn + ' is not a planning function in logicPlan.py.')
        func = getattr(plan_mod, fn)
        self.planningFunction = lambda x: func(x)

        # Get the planning problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError (prob + ' is not a planning problem type in logicAgents.py.')
        self.planType = globals()[prob]
        print('[LogicAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.planningFunction == None: raise Exception ("No planning function provided for LogicAgent")
        starttime = time.time()
        problem = self.planType(state) # Makes a new planning problem
        self.actions  = self.planningFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        # TODO Drop
        if '_expanded' in dir(problem): print('Nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(list(self.actions)):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionPlanningProblem(logicPlan.PlanningProblem):
    """
    A planning problem defines the state space, start state, goal test, successor
    function and cost function.  This planning problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this planning problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a planning state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print ('Warning: this does not look like a regular position planning maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def getGoalState(self):
        return self.goal

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999. 

        This is included in the logic project solely for autograding purposes.
        You should not be calling it.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost
    
    def getWidth(self):
        """
        Returns the width of the playable grid (does not include the external wall)
        Possible x positions for agents will be in range [1,width]
        """
        return self.walls.width-2

    def getHeight(self):
        """
        Returns the height of the playable grid (does not include the external wall)
        Possible y positions for agents will be in range [1,height]
        """
        return self.walls.height-2

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionPlanningProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionPlanningProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

class FoodPlanningProblem:
    """
    A planning problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A planning state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999. 

        This is included in the logic project solely for autograding purposes.
        You should not be calling it.
        """
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost
    
    def getWidth(self):
        """
        Returns the width of the playable grid (does not include the external wall)
        Possible x positions for agents will be in range [1,width]
        """
        return self.walls.width-2

    def getHeight(self):
        """
        Returns the height of the playable grid (does not include the external wall)
        Possible y positions for agents will be in range [1,height]
        """
        return self.walls.height-2

class FoodGhostsPlanningProblem:
    """
    A planning problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game. But watch out, there are ghosts patrolling the
    board. Every ghost has a deterministic motion, so we can plan around them.

    Ghost initial positions may be determined from the getGhostStartState().

    A planning state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.ghostStartStates = startingGameState.getGhostStates()
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start
    
    def getGhostStartStates(self):
        return self.ghostStartStates

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999

        This is included in the logic project solely for autograding purposes.
        You should not be calling it.
        """
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost
    
    def getWidth(self):
        """
        Returns the width of the playable grid (does not include the external wall)
        Possible x positions for agents will be in range [1,width]
        """
        return self.walls.width-2

    def getHeight(self):
        """
        Returns the height of the playable grid (does not include the external wall)
        Possible y positions for agents will be in range [1,height]
        """
        return self.walls.height-2
