#!/usr/bin/env python

import os


def read_puzzle_input() -> tuple[list, list]:
    """
    Read the file and create a list.

    :return: A list that contains stuff
    :rtype: list
    """
    rules = []
    updates = []
    with open("05.in", "r") as file:
        rules, updates = file.read().split('\n\n')
    rules = rules.strip().split()
    updates = [update.split(',') for update in updates.strip().split()]
    return rules, updates


def correct_order(update: list, rules: list) -> bool:
    """
    Test to see if the update is in the correct order utilizing the page
    ordering rules.

    :param list update: A single update's list of pages
    :param list rules: Page ordering rules
    :return: True if update follows the page ordering rules, otherwise False
    :rtype: bool
    """
    count = 0
    for i in range(len(update)):
        if i + 1 < len(update) and f"{update[i]}|{update[i+1]}" in rules:
            count += 1
    if count == len(update) - 1:
        return True
    return False


def fix_order(update: list, rules: list) -> list:
    """
    Fix the order of the update pages so they follow the page ordering rules.

    :param list update: A single update's list of pages that do not follow the
                        page ordering rules.
    :param list rules: Page ordering rules
    :return: The fixed update that now follows the page ordering rules.
    :rtype: list
    """
    n = len(update)
    while not correct_order(update, rules):
        for i in range(n - 1):
            if f"{update[i]}|{update[i+1]}" not in rules:
                update[i], update[i+1] = update[i+1], update[i]
        fix_order(update, rules)
    return update


def sum_middle_pages(update: list) -> int:
    """
    Find the middle page in the list of update pages.

    :param list update: A single update's list of pages
    :return: The page number of the update's middle page
    :rtype: int
    """
    return int(update[len(update)//2])


def part_one(rules: list, updates: list) -> int:
    """
    Compare the pages in each update to the page ordering rules and if they are
    in the correct order, then sum all of the middle page numbers from each
    update.

    :param list rules: Page ordering rules
    :param list updates: Pages to produce in each update
    :return: Sum of the middle page numbers from each update if rules are
             matched.
    :rtype: int
    """
    sum = 0
    for update in updates:
        if correct_order(update, rules):
            sum += sum_middle_pages(update)
    return sum


def part_two(rules: list, updates: list) -> int:
    """
    To fix the updates that failed the rules, use the page ordering rules to
    put the page numbers in the right order. Once they are fixed, only sum the
    middle page number of the fixed ones, ignoring the good ones from Part 1

    :param list rules: Page ordering rules
    :param list updates: Pages to produce in each update
    :return: Sum of the middle page numbers from each fixed update that didn't
             get summed in "part_one"
    :rtype: int
    """
    sum = 0
    for update in updates:
        if not correct_order(update, rules):
            new_update = fix_order(update, rules)
            sum += sum_middle_pages(new_update)
    return sum


if __name__ == "__main__":
    rules, updates = read_puzzle_input()
    print("Part 1:", part_one(rules, updates))  # 6498
    print("Part 2:", part_two(rules, updates))  # 5017
