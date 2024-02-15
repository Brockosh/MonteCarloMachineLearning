from __future__ import print_function, division
from builtins import range

def PrintValues(V, g):
    # Iterate through the grid's width
    for i in range(g.width):
        print("---------------------------")
        # Iterate through the grid's height
        for j in range(g.height):
            # Retrieve the value for each state, defaulting to 0 if not found
            v = V.get((i, j), 0)  
            # Format positive values with two decimal places
            if v >= 0:
                print(" %.2f|" % v, end="")
            # Format negative values appropriately
            else:
                print("%.2f|" % v, end="")  
        print("")

def PrintPolicy(P, g):
    # Iterate through the grid's width
    for i in range(g.width):
        print("---------------------------")
        # Iterate through the grid's height
        for j in range(g.height):
            # Retrieve the policy action for each state, defaulting to a blank space if not found
            a = P.get((i, j), ' ')  
            # Display the action
            print("  %s  |" % a, end="")
        print("")

def MaxDict(d):
    # Function is used frequently to find the argmax (key) and max (value) from a dictionary
    max_key = None
    max_val = float('-inf')  # Initialize with the smallest possible number
    for k, v in d.items():
        # Identify the key with the maximum value
        if v > max_val:
            max_val = v
            max_key = k
    # Return the key (argmax) and the maximum value found
    return max_key, max_val