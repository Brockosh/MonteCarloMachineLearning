from __future__ import print_function, division
from builtins import range
import numpy as np
import matplotlib.pyplot as plt
from GridWorld import CreateStandardGrid 
from Utilities import MaxDict, PrintValues, PrintPolicy

GAMMA = 0.9
EPSILON = 0.2
ALL_POSSIBLE_ACTIONS = ('U', 'D', 'L', 'R')
N_EPISODES = 8000

def SelectActionEpsilonGreedy(action, eps=0.1):
    # Generate a random number between 0 and 1.
    randomNum = np.random.random()
    # With probability 1-eps, choose the given action.
    if randomNum < (1 - eps):
        return action
    # With probability eps, choose a random action from all possible actions.
    else:
        return np.random.choice(ALL_POSSIBLE_ACTIONS)

def RunEpisode(grid, policy):
    # Initialize the starting state.
    s = (2, 0)
    grid.SetState(s)
    # Select the initial action using the policy and epsilon-greedy strategy.
    a = SelectActionEpsilonGreedy(policy[s], EPSILON)
    # Initialize the list to store state, action, and immediate reward.
    StatesActionsRewards = [(s, a, 0)]
    # Loop until the episode ends.
    while True:
        # Execute the action and observe the reward and next state.
        r = grid.Move(a)
        s = grid.CurrentState()
        # Check if the current state is terminal.
        if grid.GameOver():
            # If terminal, append the final state, action as None, and reward.
            StatesActionsRewards.append((s, None, r))
            break
        else:
            # If not terminal, select the next action and append state, action, and reward.
            a = SelectActionEpsilonGreedy(policy[s], EPSILON)
            StatesActionsRewards.append((s, a, r))
    # Initialize the variable for the return from this state.
    G = 0
    StatesActionsReturns = []
    # Flag to skip the first state as it's terminal with a return of 0.
    first = True
    # Calculate the returns for each state-action pair in the episode, starting from the end.
    for s, a, r in reversed(StatesActionsRewards):
        if first:
            # Skip the first because it's the terminal state.
            first = False
        else:
            # Append the state, action, and calculated return G to the list.
            StatesActionsReturns.append((s, a, G))
        # Update the return G using the reward and discount factor, working backwards.
        G = r + GAMMA * G
    # Reverse the list of states, actions, and returns to restore the original episode order.
    StatesActionsReturns.reverse()
    return StatesActionsReturns

def MonteCarloPolicyEvaluation(grid):
    # Initialize the policy randomly for all possible actions in each state.
    policy = {}
    for s in grid.GetNonTerminalStates():
        policy[s] = np.random.choice(ALL_POSSIBLE_ACTIONS)
    # Initialize the action value function Q(s,a) and the returns dictionary for each state-action pair.
    Q = {}
    returns = {}
    # Only consider non-terminal states
    states = grid.GetNonTerminalStates()
    for s in states:
        Q[s] = {}
        for a in ALL_POSSIBLE_ACTIONS:
            # Initial estimate of Q(s,a)
            Q[s][a] = 0
            # List to store returns for updating Q(s,a)
            returns[(s, a)] = []
    # Track the maximum change in Q value in each episode to assess convergence.
    deltas = []
    # Loop over episodes
    for t in range(N_EPISODES):
        # Print progress every 1000 episodes
        if t % 1000 == 0:
            print(t)
        # Generate an episode and calculate returns following the current policy.
        biggest_change = 0
        states_actions_returns = RunEpisode(grid, policy)
        # Keep track of state-action pairs we have seen to apply first-visit MC.
        seenPairs = set()
        for s, a, G in states_actions_returns:
            sa = (s, a)
            if sa not in seenPairs:
                # Append the return G to the returns list for state-action pair sa.
                returns[sa].append(G)
                old_q = Q[s][a]
                # Update Q(s,a) as the average of observed returns.
                Q[s][a] = np.mean(returns[sa])
                biggest_change = max(biggest_change, np.abs(old_q - Q[s][a]))
                seenPairs.add(sa)
        deltas.append(biggest_change)
        # Update the policy to perform the action that maximizes Q(s,a) for each state.
        for s in policy.keys():
            a, _ = MaxDict(Q[s])
            # Update policy
            policy[s] = a
    # Compute the value function V for each state based on the optimal action values.
    V = {}
    for s in policy.keys():
        V[s] = MaxDict(Q[s])[1]
    return V, policy, deltas

if __name__ == '__main__':
    grid = CreateStandardGrid(obeyProbability=0.8, stepCost=-0.2)
    print("Rewards:")
    PrintValues(grid.rewards, grid)
    V, policy, deltas = MonteCarloPolicyEvaluation(grid)
    print("Final Values:")
    PrintValues(V, grid)
    print("Final Policy:")
    PrintPolicy(policy, grid)
    

    # Uncomment to show graphs
    # plt.plot(deltas)
    # plt.show()

# Method explanations: 

# SelectActionEpsiloGreedy
# Selects an action based on the epsilon-greedy strategy. With probability 1-epsilon, 
# it chooses the given action (exploitation). With probability epsilon, it chooses 
# an action at random from all possible actions (exploration).

# Parameters:
# - action: The current best action to take according to the policy.
# - eps: The probability of choosing a random action (exploration rate).

# Returns:
# - The action chosen based on the epsilon-greedy policy.
    

# RunEpisode 
# Simulates an episode within the grid world environment given a policy. 
# This function generates a sequence of states, actions, and rewards based on the policy and environment dynamics.

# Parameters:
# - grid: The grid world environment where the episode is simulated.
# - policy: The policy to follow during the episode simulation.

# Returns:
# - StatesActionsReturns: A list of tuples containing states, actions, 
# and returns for each state-action pair encountered in the episode.



#MonteCarloPolicyEvaluation
#    Evaluates a policy for a given grid world using the Monte Carlo method.
#    This involves simulating episodes of the game, observing the returns for state-action pairs,
#    and iteratively improving the action value function estimates.

#    Parameters:
#    - grid: The grid world environment where the policy is evaluated.

#    Returns:
#    - V: The estimated value function for the policy.
#    - policy: The optimized policy after evaluation.
#    - deltas: The list of maximum changes in the action value function per episode, used to monitor convergence.



    