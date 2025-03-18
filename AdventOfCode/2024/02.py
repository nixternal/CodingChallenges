#!/usr/bin/env python


def read_puzzle_input() -> list:
    """
    Read the file and create a list of lists from each line. Lines are
    different lengths, but look similar to the following:

        1 3 9 2 1
        7 4 4 6 1 6 9

    :return: A list that contains a list of each line
    :rtype: list
    """
    reports = []
    with open("02.in", "r") as file:
        for line in file:
            reports.append([int(x) for x in line.strip().split()])
    return reports


def is_safe(report: list) -> bool:
    """
    Tests if the report sent is safe. A report is safe if it is increasing from
    beginning to end or decreasing from beginning to end. The minimum change
    between values is 1 and the maximum is 3. If these are met then the report
    is deemed safe.

    :param list report: A single report with a list of numbers to be tested
    :return: Is the report safely increasing or decreasing?
    :rtype: bool
    """
    increasing = True
    decreasing = True
    for i in range(1, len(report)):
        if report[i] - report[i-1] < 1 or report[i] - report[i-1] > 3:
            increasing = False
        if report[i] - report[i-1] < -3 or report[i] - report[i-1] > -1:
            decreasing = False
    return increasing or decreasing


def can_be_safe(report: list) -> bool:
    """
    Tests if the report sent can be made safe by removing a single 'bad' level.

    :param list report: A single report with a list of numbers to be tested
    :return: Is the new report now safe?
    :rtype: bool
    """
    for i in range(len(report)):
        new_report = report[:i] + report[i+1:]
        if is_safe(new_report):
            return True
    return False


def count_safe_reports(reports: list, part: int = 0) -> int:
    """
    Calculate the amount of 'safe' reports. Definition of a 'safe' report can
    be found in the 'is_safe' function.

    :param list reports: The list of lines containing the numbers to be tested
    :param int part: Used to trigger counting of the 2nd part of the puzzle
    :return: Number of lines that have tested & are deemed safe
    :rtype: int
    """
    num_safe = 0
    for report in reports:
        if is_safe(report):
            num_safe += 1
        elif part == 2 and can_be_safe(report):
            num_safe += 1
    return num_safe


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", count_safe_reports(data))     # 341
    print("Part 2:", count_safe_reports(data, 2))  # 404
