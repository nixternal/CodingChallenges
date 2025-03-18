#!/usr/bin/env python

"""
This script solves a two-part puzzle. It reads input from a file, processes
the data to create a network of connections, and performs computations to
derive results for each part of the puzzle. The code is written with the aim
to identify specific structures within the data and analyze connections
between them.

Functions are documented inline to ensure clarity for users of all experience
levels.

Part 1: The algorithm/task is commonly known as "Triangle Enumeration" or
"Triangle Counting" in graph theory. The code used here is a brute-force
triangle enumeration approach.
    1. Iterate  over each node "x" in the graph.
    2. For each node "y" connected to "x":
        * For each node "z" connected to "y":
            - Check if "z" is connected to "x"
    3. If the above condition is true, "x", "y", and "z" form a triangle.

Part 2: The algorithm used is commonly known as the "Bron-Kerbosch" algorithm.
It is a classic algorithm for finding all maximal cliques in an undirected
graph. It is often used for this type of problem and can be optimized with
pivoting techniques. It is a recursive algorithm. It uses 3 sets:
    R: The growing clique
    P: The set of candidate nodes that can expand R.
    X: The set of nodes that have already been considered for R.
Pivoting technique improves efficiency as a pivot node is chosen to reduce the
size of P (the candidate set), limiting the number of recursive calls. After
all of the maximal cliques are identified, the largest clique is selected.
"""


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named '23.in'.

    Returns:
        List[str]: A list of strings, each representing a line from the input
                   file.
    """

    with open("23.in", "r") as file:
        return file.read().splitlines()


def create_connections(data: list) -> dict:
    """
    Processes the input data to create a dictionary representing bidirectional
    connections.

    Args:
        data (List[str]): A list of strings, where each string represents a
                          connection in the format "A-B".

    Returns:
        Dict[str, Set[str]]: A dictionary where keys are nodes and values are
                             sets of connected nodes.
    """

    # Parse each line into a pair of nodes (x, y)
    edges = [line.strip().split("-") for line in data]
    conns = {}

    for x, y in edges:
        # Ensure both nodes are in the dictionary
        if x not in conns:
            conns[x] = set()
        if y not in conns:
            conns[y] = set()
        # Establish bidirectional connections
        conns[x].add(y)
        conns[y].add(x)

    return conns


def bron_kerbosch(conns: dict, r: set, p: set, x: set, cliques: list):
    """
    The Bron–Kerbosch algorithm with pivoting to find all maximal cliques in
    the graph.

    Args:
        conns (dict): The graph represented as a dictionary of nodes and their
                      connections.
        r (set): The currently growing clique (starts as an empty set).
        p (set): The set of candidate nodes that can be added to the clique.
        x (set): The set of nodes already considered for the clique.
        cliques (list): A list to store all maximal cliques.
    """

    if not p and not x:
        # Found a maximal clique
        cliques.append(r)
        return

    # Choose a pivot node (heuristic: maximize the reduction in p)
    pivot = next(iter(p.union(x)))
    non_neighbors = p - conns[pivot]

    for v in non_neighbors:
        bron_kerbosch(conns, r.union({v}), p.intersection(conns[v]),
                      x.intersection(conns[v]), cliques)
        p.remove(v)
        x.add(v)



def part_one(data: list) -> int:
    """
    Solves Part 1 of the puzzle. Identifies and counts all unique sets of
    three connected nodes (triangles) where at least one node starts with the
    letter 't'.

    Args:
        data (List[str]): A list of strings representing connections.

    Returns:
        int: The number of unique triangles containing a node starting w/ 't'.
    """

    sets = set()  # Store unique triangles
    conns = create_connections(data)

    # Iterate through all connections to identify triangles
    for x in conns:
        for y in conns[x]:
            for z in conns[y]:
                # Check if valid triangle exists
                if x != z and x in conns[z]:
                    sets.add(tuple(sorted([x, y, z])))

    # Filter triangles to count those containing a node starting with "t"
    return len([s for s in sets if any(cn.startswith("t") for cn in s)])


def part_two(data: list) -> str:
    """
    Finds the largest group of mutually connected nodes (maximum clique) using
    the Bron–Kerbosch algorithm.

    Args:
        data (list): The input data as a list of connections.

    Returns:
        str: A comma-separated string of node names in the largest group.
    """

    # Create the graph as a dictionary of connections
    conns = create_connections(data)

    # Initialize variables for the Bron-Kerbosch algorithm
    r, p, x = set(), set(conns.keys()), set()
    cliques = []

    # Find all maximal cliques
    bron_kerbosch(conns, r, p, x, cliques)

    # Find the largest clique
    max_clique = max(cliques, key=len)

    return ",".join(sorted(max_clique))


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1083
    print("Part 2:", part_two(data))  # as,bu,cp,dj,ez,fd,hu,it,kj,nx,pp,xh,yu
