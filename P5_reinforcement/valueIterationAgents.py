# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for iter in range(self.iterations):
            best_q_vals = {}
            # pass value of the best action in the states
            for state in self.mdp.getStates():
                best_action = self.computeActionFromValues(state)
                if best_action: best_q_vals[state] = self.getQValue(state, best_action)
            for state in best_q_vals:
                self.values[state] = best_q_vals[state]

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0
        # Q = prob*(r + discount*Value(s'))
        for trans_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            reward = self.mdp.getReward(state, action, trans_state)
            q_value += prob*(reward + self.discount*self.getValue(trans_state))
        return q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # no legal actions, terminal state
        if self.mdp.isTerminal(state): return None
        # normal find action with best q value
        res_act = 0; max_q_val = float('-inf')
        for action in self.mdp.getPossibleActions(state):
            act_q_val = self.getQValue(state, action)
            if act_q_val > max_q_val:
                max_q_val = act_q_val; res_act = action
        return res_act

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        for i in range(self.iterations):
            # iter > state number
            state = states[i % len(states)]
            # pass value of the best action at target state
            best_action = self.computeActionFromValues(state)
            if best_action: self.values[state] = self.getQValue(state, best_action)

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # dictionary of predecessors of all states.
        predecessors = {}
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state): continue
            pre_temp = []
            # find pre of s by push other states that transition includes s
            for state_other in self.mdp.getStates():
                for action in self.mdp.getPossibleActions(state_other):
                    for trans_state, act in self.mdp.getTransitionStatesAndProbs(state_other, action):
                        if trans_state == state: pre_temp.append(state_other)
            predecessors[state] = pre_temp
                
        pqueue = util.PriorityQueue()
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state): continue
            # difference between the current val of s in self.values and the highest Q-value across all possible actions from s
            diff_val = abs(self.values[state] - self.computeQValueFromValues(state, self.computeActionFromValues(state)))
            pqueue.push(state,-diff_val)
        
        for iter in range(self.iterations):
            # If the priority queue is empty, then terminate
            if pqueue.isEmpty(): break
            # Pop a state s off the priority queue
            state = pqueue.pop()
            # Update the value of s (if it is not a terminal state) in self.values
            if self.mdp.isTerminal(state) != None:
                self.values[state] = self.computeQValueFromValues(state, self.computeActionFromValues(state))

            for pred in predecessors[state]:
                if self.mdp.isTerminal(state): continue
                # difference between the current value of p in self.values and the highest Q-value across all possible actions from p
                diff_val = abs(self.values[pred] - self.computeQValueFromValues(pred, self.computeActionFromValues(pred)))
                if diff_val > self.theta: pqueue.update(pred,-diff_val)
