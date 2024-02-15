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




  
  
  
  
  

