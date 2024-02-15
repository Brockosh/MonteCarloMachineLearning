from __future__ import print_function, division
from builtins import range
import numpy as np
from grid_world import StandardGrid  # Ensure this class's methods start with capital letters
from Utilities import PrintValues, PrintPolicy  # Verify these functions match expected naming conventions

# Define a small threshold to determine when the value function has converged
SMALL_ENOUGH = 1e-3
GAMMA = 0.9  # Discount factor for future rewards
ALL_POSSIBLE_ACTIONS = ('U', 'D', 'L', 'R')  # Available actions in the grid world

def BestActionValue(grid, V, s):
  # Identifies the optimal action and its value from a given state by evaluating all possible actions.
  BestA = None
  BestValue = float('-inf')
  grid.SetState(s)  # Set current state to s
  # Evaluate each action by calculating expected future rewards
  for a in ALL_POSSIBLE_ACTIONS:
    Transitions = grid.GetTransitionProbabilities(a)
    ExpectedV = 0
    ExpectedR = 0
    # Calculate the expected value and reward for taking action a in state s
    for (prob, r, StatePrime) in Transitions:
      ExpectedR += prob * r  # Immediate reward
      ExpectedV += prob * V[StatePrime]  # Value of next state
    V = ExpectedR + GAMMA * ExpectedV
    if V > BestValue:
      BestValue = V
      BestA = a
  return BestA, BestValue

def CalculateValues(grid):
  # Initialize value function V(s) for all states as zero
  V = {}
  States = grid.AllStates()
  for s in States:
    V[s] = 0
  # Iteratively update V(s) using the Bellman equation until convergence
  while True:
    BiggestChange = 0  # Track largest change in value function across all states
    for s in grid.NonTerminalStates():
      OldV = V[s]
      # Update V(s) by finding the best action value
      _, NewV = BestActionValue(grid, V, s)
      V[s] = NewV
      BiggestChange = max(BiggestChange, np.abs(OldV - NewV))

    if BiggestChange < SMALL_ENOUGH:
      break  # Stop iteration when changes are below the threshold
  return V

def InitRandomPolicy():
  # Initialize a policy that maps each state to a random action
  Policy = {}
  for s in grid.NonTerminalStates():
    Policy[s] = np.random.choice(ALL_POSSIBLE_ACTIONS)
  return Policy

def CalculateGreedyPolicy(grid, V):
  # Derive a greedy policy based on the current value function
  Policy = InitRandomPolicy()
  for s in Policy.keys():
    grid.SetState(s)
    # Select the action that maximizes the value function for each state
    BestA, _ = BestActionValue(grid, V, s)
    Policy[s] = BestA
  return Policy


if __name__ == '__main__':
  # Initialize the grid world with specified parameters
  grid = StandardGrid(obey_prob=0.8, step_cost=-0.1)

  # Display the grid's reward structure
  print("Rewards:")
  PrintValues(grid.rewards, grid)

  # Compute the value function for each state
  V = CalculateValues(grid)

  # Generate an optimal policy using the value function
  policy = CalculateGreedyPolicy(grid, V)

  # Output the final value function and policy
  print("Values:")
  PrintValues(V, grid)
  print("Policy:")
  PrintPolicy(policy, grid)