# bustersGhostAgents.py
# ---------------------
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


import ghostAgents
from game import Directions
from game import Actions
from util import manhattanDistance
import util

class StationaryGhost( ghostAgents.GhostAgent ):
    def getDistribution( self, state ):
        dist = util.Counter()
        dist[Directions.STOP] = 1.0
        return dist

class DispersingGhost( ghostAgents.GhostAgent ):
    "Chooses an action that distances the ghost from the other ghosts with probability spreadProb."
    def __init__( self, index, spreadProb=0.5):
        self.index = index
        self.spreadProb = spreadProb

    def getDistribution( self, state ):
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5
        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]

        # get other ghost positions
        others = [i for i in range(1,state.getNumAgents()) if i != self.index]
        for a in others: assert state.getGhostState(a) != None, "Ghost position unspecified in state!"
        otherGhostPositions = [state.getGhostPosition(a) for a in others if state.getGhostPosition(a)[1] > 1]

        # for each action, get the sum of inverse squared distances to the other ghosts
        sumOfDistances = []
        for pos in newPositions:
            sumOfDistances.append( sum([(1+manhattanDistance(pos, g))**(-2) for g in otherGhostPositions]) )

        bestDistance = min(sumOfDistances)
        numBest = [bestDistance == dist for dist in sumOfDistances].count(True)
        distribution = util.Counter()
        for action, distance in zip(legalActions, sumOfDistances):
            if distance == bestDistance: distribution[action] += self.spreadProb / numBest
            distribution[action] += (1 - self.spreadProb) / len(legalActions)
        return distribution
