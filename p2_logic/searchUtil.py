# searchUtil.py
# -------------
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


import util
import warnings
from game import Actions
from game import Directions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    if problem.goalTest(start_state):
        return []
    
    frontier = util.PriorityQueue()
    frontier_dict = {}
    initial_actions = problem.getActions(start_state)
    for action in initial_actions:
        (next_state, cost) = problem.getResult(start_state, action)
        state_action_cost = (next_state, action, cost)
        frontier.push([state_action_cost],cost+heuristic(next_state,problem))
        frontier_dict[str([state_action_cost])] = next_state
    
    closed = [start_state]
    
    while not frontier.isEmpty():
        node = frontier.pop()
        del frontier_dict[str(node)]
#         for n in node:
#             print "%s," % n[1],
#         print
        if problem.goalTest(node[-1][0]):
            sol = extractSolution(node)
            print (sol)
            return sol
        closed += [node[-1][0]]
        actions = problem.getActions(node[-1][0])
        for action in actions:
            (next_state, cost) = problem.getResult(node[-1][0], action)
            state_action_cost = (next_state, action, cost)
            if not next_state in closed and not next_state in frontier_dict.values():
                for n in node:
                    cost += n[2]
#                 print "Push %s: f = %d + %d" % (child[0],cost,heuristic(child[0],problem))
                frontier.push(node+[state_action_cost],cost+heuristic(next_state,problem))
                frontier_dict[str(node+[state_action_cost])] = next_state
    
    print ("Solution not found!!!")
    return []

def extractSolution(node):
    sol = []
    for state in node:
        sol += [state[1]]

    return sol

class SafeSearchProblem():
    def __init__(self):
        self.goalStates = []
        self.safeStates = None
        
    def setWalls(self, walls):
        self.walls = walls
        
    def setStartState(self, startState):
        self.startState = startState
        
    def setGoalStates(self, goalStates):
        self.goalStates = goalStates
        
    def setSafeStates(self, safeStates):
        self.safeStates = safeStates
        
    def getStartState(self):
        return self.startState
    
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
        
        if self.safeStates == None:
            return actions
        
        safeActions = []
        for action in actions:
            (nextState, _) = self.getResult(state, action)
            if nextState in self.safeStates:
                safeActions.append(action) 

        return safeActions

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
        return state in self.goalStates
        
