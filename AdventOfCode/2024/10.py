#!/usr/bin/env python

# Parse the input file to create a dictionary 'M' representing a grid:
# Each key is a tuple (i, j) corresponding to the row 'i' and column 'j' in
# the grid. Each value is an integer parsed from the character at that
# position in the file.
M = {
        (i, j): int(c) for (i, l) in enumerate(open("10.in"))
        for (j, c) in enumerate(l.strip())
}

# Create a dictionary 'N' that maps each position (i, j) in the grid to its
# neighbors: A neighbor is a valid adjacent position (up, down, left, right)
# that exists in 'M'.
N = {
        (i, j): {(i-1, j), (i+1, j), (i, j-1), (i, j+1)} & M.keys()
        for (i, j) in M
}

# Define a recursive lambda function 'p' to find paths starting from a given
# position 's':
#    - If the value at 's' is 9, return a single-element list containing 's'.
#    - Otherwise, recursively explore all neighbors 'n' whose value is one
#      greater than 's'.
p = lambda s: [s] if M[s] == 9 else sum(
        [p(n) for n in N[s] if M[n] == M[s]+1], [])

# First result:
# - Iterate over all positions 'c' in 'M' where the value is 0.
# - For each such 'c', compute the set of unique positions in paths starting
#   from 'c' (via 'p').
# - Compute the sum of the lengths of these unique sets.
print(sum(len(set(p(c))) for c in M if M[c] == 0))

# Second result:
# - Similar to the first result, but instead of using unique sets, directly
#   sum the lengths of paths.
print(sum(len(p(c)) for c in M if M[c] == 0))
