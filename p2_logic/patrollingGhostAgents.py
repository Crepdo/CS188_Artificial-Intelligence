# patrollingGhostAgents.py
# ------------------------
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
import util

class PatrollingGhost( ghostAgents.GhostAgent ):
    
    def __init__(self, index, starting_action=Directions.EAST):
        ghostAgents.GhostAgent.__init__(self, index)
        self.current_action = starting_action
    
    "A ghost that deterministically patrols east and west."
    def getDistribution( self, state ):
        conf = state.getGhostState( self.index ).configuration
        possibleActions = Actions.getPossibleActions( conf, state.data.layout.walls )
        reverse = Actions.reverseDirection( self.current_action )
        
        if Directions.STOP in possibleActions:
            possibleActions.remove( Directions.STOP )

        dist = util.Counter()
        
        # We hit a wall, go the other way
        if not self.current_action in possibleActions:
            if reverse in possibleActions:
                self.current_action = reverse
            else:
                raise Exception("Ghost is stuck. Can't patrol "+self.current_action+" or "+reverse+".")
            
        dist[self.current_action] = 1.0
        conf.direction = self.current_action
        dist.normalize()
        return dist
    
class StationaryGhost( ghostAgents.GhostAgent ):
    
    def __init__(self, index, starting_action=Directions.EAST):
        ghostAgents.GhostAgent.__init__(self, index)
    
    "A ghost that stands still."
    def getDistribution( self, state ):
        dist = util.Counter()                    
        dist[Directions.STOP] = 1.0
        dist.normalize()
        return dist    
