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