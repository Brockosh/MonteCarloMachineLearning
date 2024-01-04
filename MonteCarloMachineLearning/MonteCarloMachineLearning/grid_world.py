from __future__ import print_function, division
from builtins import range
import numpy as np


class Grid: # Environment
  def __init__(self, width, height, start):
    # i is vertical axis, j is horizontal
    self.width = width
    self.height = height
    self.i = start[0]
    self.j = start[1]

  def Set(self, rewards, actions, obey_prob):
    # rewards are a dict of: (i, j): r (row, col): reward
    # actions are a dict of: (i, j): A (row, col): list of possible actions
    self.rewards = rewards
    self.actions = actions
    self.obey_prob = obey_prob

  def NonTerminalStates(self):
    return self.actions.keys()

  def SetState(self, s):
    self.i = s[0]
    self.j = s[1]

  def CurrentState(self):
    return (self.i, self.j)

  def IsTerminal(self, s):
    return s not in self.actions

  def MoveStochastically(self, action):
    p = np.random.random()
    if p <= self.obey_prob:
      return action
    if action == 'U' or action == 'D':
      return np.random.choice(['L', 'R'])
    elif action == 'L' or action == 'R':
      return np.random.choice(['U', 'D'])  
  
  def Move(self, action):
    actual_action = self.MoveStochastically(action)
    if actual_action in self.actions[(self.i, self.j)]:
      if actual_action == 'U':
        self.i -= 1
      elif actual_action == 'D':
        self.i += 1
      elif actual_action == 'R':
        self.j += 1
      elif actual_action == 'L':
        self.j -= 1
    return self.rewards.get((self.i, self.j), 0)
  
  def CheckMove(self, action):
    i = self.i
    j = self.j
    # check if legal move first
    if action in self.actions[(self.i, self.j)]:
      if action == 'U':
        i -= 1
      elif action == 'D':
        i += 1
      elif action == 'R':
        j += 1
      elif action == 'L':
        j -= 1
    # return a reward (if any)
    reward = self.rewards.get((i, j), 0)
    return ((i, j), reward)

  def GetTransitionProbabilities(self, action):
    # returns a list of (probability, reward, s') transition tuples
    probs = []
    state, reward = self.CheckMove(action)
    probs.append((self.obey_prob, reward, state))
    disobey_prob = 1 - self.obey_prob
    if not (disobey_prob > 0.0):
      return probs
    if action == 'U' or action == 'D':
      state, reward = self.CheckMove('L')
      probs.append((disobey_prob / 2, reward, state))
      state, reward = self.CheckMove('R')
      probs.append((disobey_prob / 2, reward, state))
    elif action == 'L' or action == 'R':
      state, reward = self.CheckMove('U')
      probs.append((disobey_prob / 2, reward, state))
      state, reward = self.CheckMove('D')
      probs.append((disobey_prob / 2, reward, state))
    return probs  

  def GameOver(self):
    # returns true if game is over, else false
    # true if we are in a terminal state
    return (self.i, self.j) not in self.actions

  def AllStates(self):
    # simple way to get all states
    # either a position that has possible next actions
    # or a position that yields a reward
    return set(self.actions.keys()) | set(self.rewards.keys())  


  
  
  
  
  

