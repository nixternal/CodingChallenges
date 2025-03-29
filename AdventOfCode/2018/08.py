#!/usr/bin/env python3

"""
Memory Maneuver - Day 8 of Advent of Code

This program solves a puzzle involving a tree-like license structure where
each node consists of:
    1. A header with two numbers:
       - The number of child nodes
       - The number of metadata entries
    2. Zero or more child nodes
    3. One or more metadata entries

The program calculates two values:
    - Part 1: The sum of all metadata entries in the entire tree
    - Part 2: The value of the root node based on special rules
"""


def read_puzzle_input(filename="08.in") -> list:
    """
    Read the puzzle input from a file and convert it to a list of integers.

    Args:
        filename (str): The name of the input file. Defaults to "08.in".

    Returns:
        list: A list of integers representing the license file structure.
    """

    with open(filename, "r") as file:
        return [int(num) for num in file.read().split()]


def parse_node(data: list) -> tuple:
    """
    Recursively parse a node in the license structure.

    This function processes each node by:
    1. Reading the header (child count and metadata count)
    2. Processing all child nodes recursively
    3. Reading the metadata entries
    4. Calculating both the metadata sum and node value

    For Part 1, we simply sum all metadata entries across all nodes.
    For Part 2, node values are calculated as follows:
        - If a node has no children, its value is the sum of its metadata
          entries
        - If a node has children, its metadata entries are interpreted as
          references to its children (1-indexed), and its value is the sum of
          the referenced children's values. Invalid references are ignored.

    Args:
        data (list): The remaining data to be processed, modified in-place

    Returns:
        tuple: (metadata_sum, node_value) where:
            - metadata_sum is the sum of all metadata in this node and its
              descendants
            - node_value is the value of this node calculated according to
              Part 2 rules
    """

    # Extract header information
    num_children = data.pop(0)
    num_metadata = data.pop(0)

    children = []
    total_metadata = 0

    # Process all child nodes
    for _ in range(num_children):
        child_metadata_sum, child_value = parse_node(data)
        children.append(child_value)
        total_metadata += child_metadata_sum

    # Process metadata entries
    metadata = data[:num_metadata]
    data[:] = data[num_metadata:]  # Remove processed metadata from data list
    total_metadata += sum(metadata)

    # Calculate node value according to Part 2 rules
    if num_children == 0:
        # Nodes with no children: value is sum of metadata
        node_value = sum(metadata)
    else:
        # Nodes with children: metadata are references to children (1-indexed)
        node_value = 0
        for index in metadata:
            if 1 <= index <= len(children):
                node_value += children[index - 1]

    return total_metadata, node_value


def part_one(data: list) -> int:
    """
    Calculate the sum of all metadata entries in the license structure.

    Args:
        data (list): The license structure data

    Returns:
        int: The sum of all metadata entries
    """

    # Create a copy to avoid modifying the original data
    return parse_node(data.copy())[0]


def part_two(data: list) -> int:
    """
    Calculate the value of the root node.

    Args:
        data (list): The license structure data

    Returns:
        int: The value of the root node
    """

    # Create a copy to avoid modifying the original data
    return parse_node(data.copy())[1]


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 41028
    print("Part 2:", part_two(data))  # 20849
