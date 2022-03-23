# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

from this import s
import util
import sys
import logic
import game

from logic import *

pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = Expr('A'); B = Expr('B'); C = Expr('C')
    return conjoin([(A|B), ((~A)%((~B)|C)), disjoin([(~A),(~B),C])])

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = Expr('A'); B = Expr('B'); C = Expr('C'); D = Expr('D')
    return conjoin([(C%(B|D)), A>>((~B)&(~D)), (~(B&(~C)))>>A, ~D>>C])

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    alive0 = PropSymbolExpr('WumpusAlive',0)
    alive1 = PropSymbolExpr('WumpusAlive',1)
    born0 = PropSymbolExpr('WumpusBorn',0)
    killed0 = PropSymbolExpr('WumpusKilled',0)
    return conjoin([ alive1%((alive0 & (~killed0)) | ((~alive0)&born0)),  ~(alive0&born0), born0])



def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    res_model = pycoSAT(to_cnf(sentence))
    if not res_model: return False
    return res_model

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return disjoin(literals)


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    res = []
    # make 2 expr a pair for or judgement:
    for twin_bool in itertools.combinations(literals,2):
        res.append(~twin_bool[0] | ~twin_bool[1])
    return conjoin(res)

def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    return atLeastOne(literals) & atMostOne(literals)


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    res = []
    for (symbol,value) in model.items():
        parse = PropSymbolExpr.parseExpr(symbol)
        # valid action, value = true
        if parse[0] in actions and value:
            res.append(parse)
    return [par[0] for par in sorted(res,key=lambda x:int(x[1]))]
            
def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    # actions and matched previous position
    act_pos_list = [(x,y-1,'North'), (x,y+1,'South'), (x+1,y,'West'), (x-1,y,'East')]

    valid_axiom = [PropSymbolExpr(pacman_str, x, y, t-1) & PropSymbolExpr(action, t-1)
            for x, y, action in act_pos_list if not walls_grid[x][y]]
    
    if not valid_axiom: return False
    #P[x,y,t] <=> axiom
    return PropSymbolExpr(pacman_str, x, y, t) % disjoin(valid_axiom)

def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"

    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    start_state = problem.getStartState()
    goal_state = problem.getGoalState()
    
    # find all valid positions that are not wall
    valid_positions = [(x,y) for x,y in itertools.product(range(1,width+1), range(1,height+1)) if not walls[x][y]]
    logic_all = PropSymbolExpr(pacman_str, start_state[0], start_state[1], 0)

    # positions other than start be reversed, join the init CNF logic
    for i in range(1, width+1):
        for j in range(1, height+1):
            if (i,j)!=start_state: 
                logic_all=conjoin(logic_all,~PropSymbolExpr(pacman_str,i,j,0))

    t = 0 # time
    actions = ['North', 'South', 'West', 'East']
    while True:
        this_action = [exactlyOne([PropSymbolExpr(act,t) for act in actions])]
        successor = [pacmanSuccessorStateAxioms(x, y, t+1, walls) for x,y in valid_positions]
        # update logic
        logic_all = conjoin(logic_all, *this_action, *successor)
        # find model with goal info
        goal = PropSymbolExpr(pacman_str,goal_state[0], goal_state[1], t+1)
        model = findModel(conjoin(logic_all, goal))
        if model != False:
            return extractActionSequence(model,actions)
        t += 1

def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    start_state,food = problem.getStartState()
    food_list = food.asList()

    # find all valid positions that are not wall
    valid_positions = [(x,y) for x,y in itertools.product(range(1,width+1), range(1,height+1)) if not walls[x][y]]
    logic_all = PropSymbolExpr(pacman_str, start_state[0], start_state[1], 0)

    # positions other than start be reversed, join the init CNF logic
    for i in range(1, width+1):
        for j in range(1, height+1):
            if (i,j)!=start_state: 
                logic_all=conjoin(logic_all,~PropSymbolExpr(pacman_str,i,j,0))

    t = 0 # time
    actions = ['North', 'South', 'West', 'East']
    while True:
        this_action = [exactlyOne([PropSymbolExpr(act,t) for act in actions])]
        successor = [pacmanSuccessorStateAxioms(x, y, t+1, walls) for x,y in valid_positions]
        # update logic
        logic_all = conjoin(logic_all, *this_action, *successor)
        # the constraints of foods:
        food_goal = []
        for food_it in food_list:
                food_goal.append(atLeastOne([PropSymbolExpr(pacman_str, food_it[0], food_it[1], i) 
                for i in range(0,t+1)]))
        food_goal = conjoin(*food_goal)

        model = findModel(conjoin(logic_all, food_goal))
        if model != False:
            return extractActionSequence(model,actions)
        t += 1


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    