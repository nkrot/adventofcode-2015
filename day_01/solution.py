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


def solve_p1(line: str) -> int:
    """Solution to the 1st part of the challenge"""
    line = line.strip()
    return line.count('(') - line.count(')')


def solve_p2(line: str) -> int:
    """Solution to the 2nd part of the challenge"""
    idx, cnt = 0, 0
    for idx, char in enumerate(line):
        if char == '(':
            cnt += 1
        elif char == ')':
            cnt -= 1
        if cnt == -1:
            break
    return 1+idx


tests = [
    ("(((", 3, None),
    ("(()(()(", 3, None),
    ("(())", 0, None),
    ("()()", 0, None),
    (")", None, 1),
    ("()())", None, 5)
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '01'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 138
    res1 = solve_p1(lines[0])
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 1771
    res2 = solve_p2(lines[0])
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
