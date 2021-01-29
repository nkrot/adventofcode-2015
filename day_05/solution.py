#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def is_nice(s: str) -> bool:
    if re.search(r'(ab|cd|pq|xy)', s):
        return False

    c_vowels = sum([1 for ch in s if ch in 'aeiou'])
    if c_vowels < 3:
        return False

    for idx in range(1, len(s)):
        if s[idx] == s[idx-1]:
            return True

    return False


def is_nice2(s: str) -> bool:
    oks = [0, 0]

    for idx in range(2, len(s)):
        if s[idx-2:idx] in s[idx:]:
            oks[0] = 1

        if s[idx] == s[idx-2]:
            oks[1] = 1

        if sum(oks) == 2:
            return True

    return False


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    return sum([1 for line in lines if is_nice(line)])


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return sum([1 for line in lines if is_nice2(line)])


tests = [
    ('ugknbfddgicrmopn', 1, None),
    ('aaa',              1, None),
    ('jchzalrnumimnmhp', 0, None),
    ('haegwjzuvuyypxyu', 0, None),
    ('dvszwmarrgswjxmb', 0, None),

    ('qjhvhtzxzqqjkmpb', None, 1),
    ('xxyxx',            None, 1),
    ('uurcxstgmygtbstg', None, 0),
    ('ieodomkazucvgmuy', None, 0)

]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        inp = [inp]

        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '05'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 255
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 55
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
