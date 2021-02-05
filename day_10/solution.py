#!/usr/bin/env python

# # #
# TODO: there must be a better/cleverer solution to part 2
# https://www.youtube.com/watch?v=ea7lJkEhytA
#

import re
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False

def split(line: str) -> List[str]:
    groups = [['']]
    grp = groups[-1]
    for ch in list(line):
        if ch != grp[-1]:
            grp = []
            groups.append(grp)
        grp.append(ch)
    groups.pop(0)
    return groups


def join(groups: List[List[str]]) -> str:
    return "".join([f"{len(grp)}{grp[0]}" for grp in groups])


def solve_p1(line: str, times=1) -> int:
    """Solution to the 1st part of the challenge"""
    res = line
    for t in range(times):
        groups = split(line)
        res = join(groups)
        line = res
    return res


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    # https://www.youtube.com/watch?v=ea7lJkEhytA
    return 0


tests = [
    ("1", "11", None),
    ("11", "21", None),
    ("21", "1211", None),
    ("1211", "111221", None),
    ("111221", "312211", None)
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
    day = '10'
    line = '1113122113'

    print(f"--- Day {day} p.1 ---")
    exp1 = 360154
    res1 = len(solve_p1(line, 40))
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 5103798
    res2 = len(solve_p1(line, 50))
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
