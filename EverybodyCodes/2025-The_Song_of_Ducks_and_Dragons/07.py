#!/usr/bin/env python


def read_puzzle_input() -> list:
    """Read and split input file into sections."""
    with open("07.in", "r") as file:
        return file.read().split("\n\n")


def parse_rules(rules_text: str) -> dict[str, set[str]]:
    """
    Parse rules from text format 'A > B,C,D' into a dictionary.
    Returns dict mapping each character to set of valid next characters.
    """
    rules = {}
    for line in rules_text.splitlines():
        current_char, next_chars = line.split(" > ")
        rules[current_char] = set(next_chars.split(","))
    return rules


def is_valid_name(name: str, rules: dict[str, set[str]]) -> bool:
    """
    Check if a name follows the rules.
    Each character must be followed by a character in its allowed set.
    """
    for i in range(len(name) - 1):
        current_char = name[i]
        next_char = name[i + 1]

        allowed_next_chars = rules.get(current_char, set())
        if next_char not in allowed_next_chars:
            return False

    return True


def part_one(data: list) -> str:
    """Find the first valid name from the list."""
    candidate_names = data[0].split(",")
    rules = parse_rules(data[1])

    for name in candidate_names:
        if is_valid_name(name, rules):
            return name

    return ""


def part_two(data: list) -> int:
    """Sum the 1-based indices of all valid names."""
    candidate_names = data[2].split(",")
    rules = parse_rules(data[3])

    valid_indices = []
    for idx, name in enumerate(candidate_names, start=1):
        if is_valid_name(name, rules):
            valid_indices.append(idx)

    return sum(valid_indices)


def generate_all_extensions(
    name: str, rules: dict[str, set[str]], max_length: int = 11
) -> set[str]:
    """
    Generate all possible valid extensions of a name up to max_length.
    Uses iterative BFS approach for better performance.
    """
    all_extensions = set()
    current_names = {name}

    # Keep extending until no more names can be extended
    while current_names:
        next_names = set()

        for current_name in current_names:
            # Add current name to results
            all_extensions.add(current_name)

            # If at max length, don't extend further
            if len(current_name) >= max_length:
                continue

            # Get valid next characters
            last_char = current_name[-1]
            allowed_next_chars = rules.get(last_char, set())

            # Generate all valid extensions
            for next_char in allowed_next_chars:
                extended_name = current_name + next_char
                if extended_name not in all_extensions:
                    next_names.add(extended_name)

        current_names = next_names

    return all_extensions


def part_three(data: list) -> int:
    """
    Count unique names of length >= 7 that can be generated from valid seed names.
    Each seed name can be extended following the rules up to length 11.
    """
    seed_names = data[4].split(",")
    rules = parse_rules(data[5])

    all_unique_names = set()

    for seed_name in seed_names:
        # Only process seed names that are valid
        if is_valid_name(seed_name, rules):
            # Generate all possible extensions
            extensions = generate_all_extensions(seed_name, rules, max_length=11)
            all_unique_names.update(extensions)

    # Count names with length >= 7
    return sum(1 for name in all_unique_names if len(name) >= 7)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # Kydravor
    print("Part 2:", part_two(data))  # 2813
    print("Part 3:", part_three(data))  # 9793790
