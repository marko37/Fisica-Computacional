#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys


# Converting into ternary
# https://www.codevscolor.com/python-convert-decimal-ternarybase-3/
def find_ternary(b):
    quotient = b/3
    remainder = b%3
    if quotient == 0: return ""
    else: return find_ternary(int(quotient)) + str(int(remainder))


def cellular_automaton(rule=30, n=100, mode=1):
    """Return a matrix representing the evolution of the
    cellular automaton n times.
    
    rule : The code of the next generation cell state table.
    
    n : The size of initial state array is 2*n + 1.
        The number of iterations that create new generations is n.
    
    mode : 1 for Elementary Cellular Automaton
           2 for Totalistic Cellular Automaton
    """

    # Creating of the initial state (generation zero).
    ca = np.zeros((n+1, 2*n + 3), dtype=int)

    # If is Elementary Cellular Automaton.
    if mode == 1:
        # Setting the state of the middle cell in the initial state.
        ca[0, ca.shape[1]//2] = 1     # // is floor division.
        # Converting rule to binary.
        x = '{0:08b}'.format(rule)
        # Creating the next generation cell state table.
        comb = {7: int(x[0]), 6: int(x[1]), 5: int(x[2]), 4: int(x[3]),
                3: int(x[4]), 2: int(x[5]), 1: int(x[6]), 0: int(x[7])}
        # In the iteration, multiplying the state of the three cells
        # by these values, we convert a number from binary to decimal.
        p1, p2 = 2, 4

    # If is Totalistic Cellular Automaton.
    else:
        ca[0, ca.shape[1]//2] = 1
        # Converting rule to ternary.
        x = find_ternary(rule).zfill(7)
        comb = {6: int(x[0]), 5: int(x[1]), 4: int(x[2]), 3: int(x[3]),
                2: int(x[4]), 1: int(x[5]), 0: int(x[6])}
        # In the iteration, multiplying the state of the three cells
        # by these values, we obtain the sum.
        p1, p2 = 1, 1

    # The iteration that calculates the state of the cells.
    for i in range(n):
        for j in range(1, ca.shape[1]-1):
            index = ca[i, j-1]*p2 + ca[i, j]*p1 + ca[i, j+1]
            ca[i+1, j] = comb[index]

    return ca


if len(sys.argv) > 1:
    # Getting the arguments from the command line.
    size = int(sys.argv[1])
    mode = int(sys.argv[2])
    rule = int(sys.argv[3])
else:
    # We will get the final size, or a time step, then choose the
    # elementary cellular automaton (Modo1) or the totallistic cellular
    # automaton (Modo2).
    size = int(input('What is the size of the grid? '))
    mode = int(input('1 (ECA) or 2 (TCA)? '))

    if mode == 1:
        rule = int(input('Type de rule for the Elementary Cellular ' +
            'Automaton, from 0 to 255: '))
    else:
        rule = int(input('Type de rule for the Totalistic Cellular ' +
            'Automaton, from 0 to 2187: '))

ca = cellular_automaton(rule, size, mode)

fig, ax = plt.subplots(1, 1, dpi=120)
ax.imshow(ca, cmap=plt.cm.Greys, interpolation='nearest')
plt.show()
