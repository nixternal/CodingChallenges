#!/usr/bin/env python

import re


def read_puzzle_input() -> list:
    with open("07.in", "r") as file:
        return file.read().splitlines()


def extract_abba_sequences(ip: str) -> list:
    # Find all ABBA sequences in a string
    abba_sequences = []

    for i in range(len(ip) - 3):
        # Extract a 4-character substring
        substring = ip[i:i + 4]

        # Check if it's an ABBA sequence
        if substring == substring[::-1] and len(set(substring)) > 1:
            abba_sequences.append(substring)
    return abba_sequences


def supports_tls(ip: str) -> bool:
    # Extract text outside and inside square brackets
    ip_segments = re.split(r'\[.*?\]', ip)
    hypernets = re.findall(r'\[(.*?)\]', ip)

    # Check for ABBA sequences in ip_segments
    ip_is_abba = False
    for segment in ip_segments:
        if extract_abba_sequences(segment):
            ip_is_abba = True
            break

    # Check for ABBA sequences inside hypernets
    hypernet_is_abba = False
    for hypernet in hypernets:
        if extract_abba_sequences(hypernet):
            hypernet_is_abba = True
            break

    # TLS is supported if there's ABBA in ip_segments & not in hypernets
    return ip_is_abba and not hypernet_is_abba


def extract_aba_sequences(ip: str) -> list:
    # Find all ABA sequences outside of square brackets
    aba_sequences = []

    # Use regex to find all text outside of square brackets
    non_hypernets = re.split(r'\[.*?\]', ip)
    for part in non_hypernets:
        for i in range(len(part) - 2):
            # Check for ABA pattern
            if part[i] == part[i + 2] and part[i] != part[i + 1]:
                aba_sequences.append(part[i:i + 3])
    return aba_sequences


def extract_bab_sequences(ip: str) -> list:
    # Find all BAB sequences inside square brackets
    bab_sequences = []

    # Use regex to find all text inside square brackets
    hypernets = re.findall(r'\[(.*?)\]', ip)
    for net in hypernets:
        for i in range(len(net) - 2):
            # Check for BAB pattern
            if net[i] == net[i + 2] and net[i] != net[i + 1]:
                bab_sequences.append(net[i:i+3])
    return bab_sequences


def supports_ssl(ip: str):
    # Extract ABA and BAB sequences
    aba_sequences = extract_aba_sequences(ip)
    bab_sequences = extract_bab_sequences(ip)

    # Check if any ABA has a corresponding BAB
    for aba in aba_sequences:
        # Convert ABA to BAB
        bab = f"{aba[1]}{aba[0]}{aba[1]}"
        if bab in bab_sequences:
            return True
    return False


def part_one(data: list) -> int:
    valid = 0
    for ip_address in data:
        if supports_tls(ip_address):
            valid += 1
    return valid


def part_two(data: list) -> int:
    valid = 0
    for ip_address in data:
        if supports_ssl(ip_address):
            valid += 1
    return valid


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 110
    print("Part 2:", part_two(data))  # 242
