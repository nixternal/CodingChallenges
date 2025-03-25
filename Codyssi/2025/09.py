#!/usr/bin/env python

from typing import List, Tuple, Dict


def read_puzzle_input() -> Tuple[str, str]:
    """
    Read input from a file named '09.in'.

    Returns:
        A tuple containing two strings:
        - First string: Initial account balances
        - Second string: Transaction records
    """

    with open("09.in", "r") as file:
        balances, transactions = file.read().strip().split('\n\n')
        return balances, transactions


def parse_balances(balances_str: str) -> Dict[str, int]:
    """
    Parse initial account balances from a string.

    Args:
        balances_str: A string containing initial balance entries.

    Returns:
        A dictionary mapping account codenames to their initial balance.
    """

    balances = {}
    for balance in balances_str.split('\n'):
        codename, _, amount = balance.split()
        balances[codename] = int(amount)
    return balances


def process_transactions(balances: Dict[str, int], transactions_str: str,
                         partial_transfer: bool = False) -> Dict[str, int]:
    """
    Process a series of transactions with optional partial transfer handling.

    Args:
        balances: A dictionary of current account balances
        transactions_str: A string containing transaction records
        partial_transfer: If True, allows partial transfers when sender lacks
                          full amount

    Returns:
        Updated account balances after processing transactions
    """

    for transaction in transactions_str.split('\n'):
        _, _from, _, _to, _, amount = transaction.split()
        amount = int(amount)

        if partial_transfer and balances[_from] <= amount:
            # When partial transfer is allowed & sender has insufficient funds
            balances[_to] += balances[_from]
            balances[_from] = 0
        else:
            # Standard transfer
            balances[_from] -= amount
            balances[_to] += amount

    return balances


def advanced_transaction_processing(balances: Dict[str, int],
                                    transactions_str: str) -> Dict[str, int]:
    """
    Advanced transaction processing with complex debt resolution.

    This method attempts to resolve transactions by checking and adjusting
    transfers based on available account balances, with a more sophisticated
    debt handling mechanism.

    Args:
        balances: A dictionary of current account balances
        transactions_str: A string containing transaction records

    Returns:
        Updated account balances after processing all transactions
    """

    transactions = [
        (_from, _to, int(amount))
        for transaction in transactions_str.split('\n')
        for _, _from, _, _to, _, amount in [transaction.split()]
    ]

    debts = []
    for debt in transactions:
        debts.append(debt)

        while True:
            next_debts = []
            for i, (_from, _to, amount) in enumerate(debts):
                if not balances[_from]:
                    # If sender has no balance, add to next debt cycle
                    next_debts.append((_from, _to, amount - balances[_from]))
                    continue

                if amount <= balances[_from]:
                    # Standard transfer possible
                    balances[_from] -= amount
                    balances[_to] += amount
                else:
                    # Partial transfer
                    balances[_to] += balances[_from]
                    next_debts.append((_from, _to, amount - balances[_from]))
                    balances[_from] = 0

                next_debts.extend(debts[i+1:])
                break

            if debts == next_debts:
                break
            debts = next_debts

    return balances


def part_one(data: tuple) -> int:
    # Standard transactions
    balances_str, transactions_str = data
    balances = parse_balances(balances_str)
    return sum(sorted(
        process_transactions(
            balances,
            transactions_str
        ).values(),
        reverse=True
    )[:3])


def part_two(data: tuple) -> int:
    # Partial transfer handling
    balances_str, transactions_str = data
    balances = parse_balances(balances_str)
    return sum(sorted(
        process_transactions(
            balances,
            transactions_str,
            partial_transfer=True
        ).values(),
        reverse=True
    )[:3])


def part_three(data: tuple) -> int:
    # Advances transaction processing
    balances_str, transactions_str = data
    balances = parse_balances(balances_str)
    return sum(sorted(
        advanced_transaction_processing(
            balances,
            transactions_str
        ).values(),
        reverse=True
    )[:3])


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 9971
    print("Part 2:", part_two(data))    # 5460
    print("Part 3:", part_three(data))  # 6310
