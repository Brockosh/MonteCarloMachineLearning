from __future__ import print_function, division
from builtins import range
import numpy as np

class EnvironmentGrid:  # Represents the grid-based environment
    def __init__(self, width, height, startPosition):
        
        # Initialize the grid environment.
        # :parameter width: Integer representing the width of the grid.
        # :parameter height: Integer representing the height of the grid.
        # :parameter startPosition: Tuple (int, int) representing the starting position (row, column) in the grid.
        
        self.width = width
        self.height = height
        self.row = startPosition[0]  # Vertical axis
        self.col = startPosition[1]  # Horizontal axis

    def Configure(self, rewards, actions, obedienceProbability):
        
        # Set the environment with rewards, actions, and the probability of obeying the chosen action.
        # :parameter rewards: Dictionary mapping from (row, col) to rewards.
        # :parameter actions: Dictionary mapping from (row, col) to available actions.
        # :parameter obedienceProbability: Float representing the probability of obeying the given action.
        
        self.rewards = rewards
        self.actions = actions
        self.obeyProb = obedienceProbability

    def GetNonTerminalStates(self):
        # Returns a list of all non-terminal states in the environment.
        return self.actions.keys()

    def SetState(self, state):
        
        # Set the current state of the environment.
        # :parameter state: Tuple (int, int) representing the new state (row, column) of the agent.
        
        self.row = state[0]
        self.col = state[1]

    def CurrentState(self):
        
        # Returns the current state of the agent in the environment.
        
        return (self.row, self.col)

    def IsTerminal(self, state):
        
        # Check if a given state is terminal.
        # :parameter state: Tuple (int, int) representing the state to check.
        
        return state not in self.actions

    def ChooseStochastically(self, action):
        
        # Chooses an action stochastically based on the obedience probability.
        # :parameter action: String representing the intended action.
       
        p = np.random.random()
        if p <= self.obeyProb:
            return action
        else:
            # If the action is not obeyed, choose an orthogonal direction
            if action in ['U', 'D']:
                return np.random.choice(['L', 'R'])
            elif action in ['L', 'R']:
                return np.random.choice(['U', 'D'])

    def Move(self, action):
        
        # Moves the agent in the environment according to the action, considering stochasticity.
        # :parameter action: String representing the action to take.
        
        actualAction = self.ChooseStochastically(action)
        if actualAction in self.actions[(self.row, self.col)]:
            if actualAction == 'U':
                self.row -= 1
            elif actualAction == 'D':
                self.row += 1
            elif actualAction == 'R':
                self.col += 1
            elif actualAction == 'L':
                self.col -= 1
        return self.rewards.get((self.row, self.col), 0)

    def SimulateAction(self, action):
        
        # Simulates the effect of an action without moving the agent.
        # :parameter action: String representing the action to simulate.
        
        row, col = self.row, self.col
        if action in self.actions[(self.row, self.col)]:
            if action == 'U':
                row -= 1
            elif action == 'D':
                row += 1
            elif action == 'R':
                col += 1
            elif action == 'L':
                col -= 1
        reward = self.rewards.get((row, col), 0)
        return ((row, col), reward)

    def GetTransitionProbabilities(self, action):
        
        # Get the transition probabilities for a given action.
        # :parameter action: String representing the action for which to get the probabilities.
        
        transitions = []
        state, reward = self.SimulateAction(action)
        transitions.append((self.obeyProb, reward, state))
        disobeyProb = 1 - self.obeyProb
        if disobeyProb > 0:
            orthogonalActions = ['L', 'R'] if action in ['U', 'D'] else ['U', 'D']
            for orthogonalAction in orthogonalActions:
                state, reward = self.SimulateAction(orthogonalAction)
                transitions.append((disobeyProb / 2, reward, state))
        return transitions

    def GameOver(self):
        
        # Check if the game is over, i.e., if the current state is terminal.
        
        return (self.row, self.col) not in self.actions

    def AllStates(self):
        
        # Get all states in the environment.
        
        return set(self.actions.keys()) | set(self.rewards.keys())

def CreateStandardGrid(obeyProbability=1.0, stepCost=None):
    grid = EnvironmentGrid(3, 4, (2, 0))
    rewards = {(0, 3): 1, (1, 3): -1}
    actions = {
        (0, 0): ('D', 'R'),
        (0, 1): ('L', 'R'),
        (0, 2): ('L', 'D', 'R'),
        (1, 0): ('U', 'D'),
        (1, 2): ('U', 'D', 'R'),
        (2, 0): ('U', 'R'),
        (2, 1): ('L', 'R'),
        (2, 2): ('L', 'R', 'U'),
        (2, 3): ('L', 'U'),
    }
    grid.Configure(rewards, actions, obeyProbability)
    if stepCost is not None:
        grid.rewards.update({
            (0, 0): stepCost,
            (0, 1): stepCost,
            (0, 2): stepCost,
            (1, 0): stepCost,
            (1, 2): stepCost,
            (2, 0): stepCost,
            (2, 1): stepCost,
            (2, 2): stepCost,
            (2, 3): stepCost,
        })
    return grid


# from __future__ import print_function, division
# from builtins import range
# import numpy as np


# class Grid: # Environment
#   def __init__(self, width, height, start):
#     # i is vertical axis, j is horizontal
#     self.width = width
#     self.height = height
#     self.i = start[0]
#     self.j = start[1]

#   def Set(self, rewards, actions, obey_prob):
#     # Rewards are a dict of: (i, j): r (row, col): reward
#     # Actions are a dict of: (i, j): A (row, col): list of possible actions
#     self.rewards = rewards
#     self.actions = actions
#     self.obey_prob = obey_prob

#   def NonTerminalStates(self):
#     return self.actions.keys()

#   def SetState(self, s):
#     self.i = s[0]
#     self.j = s[1]

#   def CurrentState(self):
#     return (self.i, self.j)

#   def IsTerminal(self, s):
#     return s not in self.actions

#   def MoveStochastically(self, action):
#     p = np.random.random()
#     if p <= self.obey_prob:
#       return action
#     if action == 'U' or action == 'D':
#       return np.random.choice(['L', 'R'])
#     elif action == 'L' or action == 'R':
#       return np.random.choice(['U', 'D'])  
  
#   def Move(self, action):
#     actual_action = self.MoveStochastically(action)
#     if actual_action in self.actions[(self.i, self.j)]:
#       if actual_action == 'U':
#         self.i -= 1
#       elif actual_action == 'D':
#         self.i += 1
#       elif actual_action == 'R':
#         self.j += 1
#       elif actual_action == 'L':
#         self.j -= 1
#     return self.rewards.get((self.i, self.j), 0)
  
#   def CheckMove(self, action):
#     i = self.i
#     j = self.j
#     # Check if legal move first
#     if action in self.actions[(self.i, self.j)]:
#       if action == 'U':
#         i -= 1
#       elif action == 'D':
#         i += 1
#       elif action == 'R':
#         j += 1
#       elif action == 'L':
#         j -= 1
#     # Returns a reward (if any)
#     reward = self.rewards.get((i, j), 0)
#     return ((i, j), reward)

#   def GetTransitionProbabilities(self, action):
#     # Returns a list of (probability, reward, s') transition tuples
#     probs = []
#     state, reward = self.CheckMove(action)
#     probs.append((self.obey_prob, reward, state))
#     disobeyProb = 1 - self.obey_prob
#     if not (disobeyProb > 0.0):
#       return probs
#     if action == 'U' or action == 'D':
#       state, reward = self.CheckMove('L')
#       probs.append((disobeyProb / 2, reward, state))
#       state, reward = self.CheckMove('R')
#       probs.append((disobeyProb / 2, reward, state))
#     elif action == 'L' or action == 'R':
#       state, reward = self.CheckMove('U')
#       probs.append((disobeyProb / 2, reward, state))
#       state, reward = self.CheckMove('D')
#       probs.append((disobeyProb / 2, reward, state))
#     return probs  

#   def GameOver(self):
#     # returns true if game is over, else false
#     # true if we are in a terminal state
#     return (self.i, self.j) not in self.actions

#   def AllStates(self):
#     # simple way to get all states
#     # either a position that has possible next actions
#     # or a position that yields a reward
#     return set(self.actions.keys()) | set(self.rewards.keys())  


# def StandardGrid(obeyProbability=1.0, stepCost=None):
#   # Grid shows rewards for arriving at each state, and potential actions to be taken at each state
#   # x = non traversible, s = start position, n = reward at that state 
#   # .  .  .  1
#   # .  x  . -1
#   # s  .  .  .
#   # obeyProbability = likelihood of obeying command
#   # stepCost = penalty applied each step to disincentivize the number of moves (-0.1)
#   g = Grid(3, 4, (2, 0))
#   rewards = {(0, 3): 1, (1, 3): -1}
#   actions = {
#     (0, 0): ('D', 'R'),
#     (0, 1): ('L', 'R'),
#     (0, 2): ('L', 'D', 'R'),
#     (1, 0): ('U', 'D'),
#     (1, 2): ('U', 'D', 'R'),
#     (2, 0): ('U', 'R'),
#     (2, 1): ('L', 'R'),
#     (2, 2): ('L', 'R', 'U'),
#     (2, 3): ('L', 'U'),
#   }
#   g.Set(rewards, actions, obeyProbability)
#   if stepCost is not None:
#     g.rewards.update({
#       (0, 0): stepCost,
#       (0, 1): stepCost,
#       (0, 2): stepCost,
#       (1, 0): stepCost,
#       (1, 2): stepCost,
#       (2, 0): stepCost,
#       (2, 1): stepCost,
#       (2, 2): stepCost,
#       (2, 3): stepCost,
#     })
#   return g


  
  
  
  
  

