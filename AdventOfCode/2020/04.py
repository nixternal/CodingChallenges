#!/usr/bin/env python

import re

REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

VALIDATION_RULES = {
    "byr": lambda v: v.isdigit() and 1920 <= int(v) <= 2002,
    "iyr": lambda v: v.isdigit() and 2010 <= int(v) <= 2020,
    "eyr": lambda v: v.isdigit() and 2020 <= int(v) <= 2030,
    "hgt": lambda v: (
        (v.endswith("cm") and v[:-2].isdigit() and 150 <= int(v[:-2]) <= 193)
        or (v.endswith("in") and v[:-2].isdigit() and 59 <= int(v[:-2]) <= 76)
    ),
    "hcl": lambda v: bool(re.fullmatch(r"#[0-9a-f]{6}", v)),
    "ecl": lambda v: v in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "pid": lambda v: bool(re.fullmatch(r"\d{9}", v)),
}


def read_puzzle_input():
    with open("04.in") as f:
        return f.read().split("\n\n")


def parse_passport(passport_string):
    """Parse passport string into a dictionary of fields."""
    tokens = passport_string.replace("\n", " ").split()
    return dict(token.split(":") for token in tokens)


def has_required_fields(fields):
    """Check if all required fields are present."""
    return REQUIRED_FIELDS.issubset(fields.keys())


def is_valid_passport(fields, validate_values=False):
    """Check if passport is valid with optional value validation."""
    if not has_required_fields(fields):
        return False

    if not validate_values:
        return True

    return all(VALIDATION_RULES[key](fields[key]) for key in REQUIRED_FIELDS)


def part_one(data):
    return sum(has_required_fields(parse_passport(passport)) for passport in data)


def part_two(data):
    return sum(
        is_valid_passport(parse_passport(passport), validate_values=True)
        for passport in data
    )


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 247
    print("Part 2:", part_two(data))  # 145
