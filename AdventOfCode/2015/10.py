#!/usr/bin/env python
"""
Look and Say Sequence - Conway Sequence (John Conway)
"""


def look_and_say(number: str) -> str:
    """
    Generates the "look-and-say" sequence for a given input string.

    The "look-and-say" sequence involves describing the input string in terms
    of consecutive digits. For example:
        Input: "111221"
        Output: "312211" (Three '1's, Two '2's, and One '1')

    Args:
        number (str): A string of digits representing the current sequence.

    Returns:
        str: The next sequence in the "look-and-say" progression.
    """

    n = len(number)  # Length of the input string
    result = []  # To store parts of the resulting string
    i = 0  # Index pointer for traversing the string

    # Traverse the string to group consecutive digits
    while i < n:
        count = 1  # Initialize the count for the current digit
        # Count the number of consecutive identical digits
        while i + 1 < n and number[i] == number[i + 1]:
            i += 1
            count += 1
        # Append the count and the digit to the result
        result.append(str(count))
        result.append(number[i])
        i += 1  # Move to the next digit

    # Combine the result list into a single string and return it
    return ''.join(result)


def main(number: str, iterations: int) -> int:
    """
    Computes the length of the "look-and-say" sequence after a specified
    number of iterations.

    Args:
        number (str): The initial input string for the sequence.
        iterations (int): The number of times to apply the "look-and-say"
                          transformation.

    Returns:
        int: The length of the sequence after the given number of iterations.
    """

    for _ in range(iterations):
        # Generate the next sequence using the look_and_say function
        number = look_and_say(number)
    # Return the length of the final sequence
    return len(number)


if __name__ == "__main__":
    print("Part 1:", main('1113222113', 40))  # 252594
    print("Part 2:", main('1113222113', 50))  # 3579328
