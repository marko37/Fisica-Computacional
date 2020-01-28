#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys, hashlib
    
def dec_to_any_base(n, base, width=0):
    """Convert from decimal to any base and return an array.
    
    width : The minimum number of elements in the returned array,
            with zero-padding if necessary.
    """

    if n == 0 and width <= 0: return []
    return dec_to_any_base(n//base, base, width-1) + [n%base]


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
        
        # Converting rule to binary and
        # creating the next generation cell state table.
        # [::-1] reverses the list order.
        comb = dec_to_any_base(rule, 2, 8)[::-1]
        
        # In the iteration, multiplying the state of the three cells
        # by these values, we convert a number from binary to decimal.
        p1, p2 = 2, 4

    # If is Totalistic Cellular Automaton.
    else:
        ca[0, ca.shape[1]//2] = 1
        
        # Converting rule to ternary and
        # creating the next generation cell state table.
        comb = dec_to_any_base(rule, 3, 7)[::-1]
        
        # In the iteration, multiplying the state of the three cells
        # by these values, we obtain the sum.
        p1, p2 = 1, 1

    # The iteration that finds the state of the cells.
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

#print (hashlib.md5(ca.tostring()).hexdigest())

fig, ax = plt.subplots(1, 1, dpi=120)
ax.imshow(ca, cmap=plt.cm.Greys, interpolation='nearest')
plt.show()
