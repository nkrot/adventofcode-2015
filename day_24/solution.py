#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from functools import reduce

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def group_by_weight(packages, maxweight):

    if not packages or maxweight < 0:
        yield None

    elif maxweight == 0:
        yield ()

    else:
        for i in range(len(packages)):
            pkg = packages[i]
            if pkg == maxweight:
                yield (pkg, )
                continue
            for grp in group_by_weight(packages[1+i:], maxweight-pkg):
                if grp is not None:
                    yield (pkg, ) + grp


def qe(packages):
    return reduce(lambda x, y: x*y, packages, 1)


def solve_p1(lines: List[str], n_groups=3) -> int:
    """Solution to the 1st part of the challenge"""
    packages = [int(line) for line in lines if line]
    weight = sum(packages)

    packages = sorted(packages, reverse=True)
    # print(packages, weight)

    groups = []
    for grp in group_by_weight(packages, weight/n_groups):
        # print("Group", grp, sum(grp), qe(grp))
        groups.append(grp)
        # break

    minsize = min(map(len, groups))
    # print(minsize)

    # select groups of with minimal number of packages and compute their
    # Quantum Entanglement values
    qes = [qe(grp) for grp in groups if len(grp) == minsize]

    return min(qes)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, 4)


text_1 = """\
1
2
3
4
5
7
8
9
10
11
"""


tests = [
    (text_1.split('\n'), 11*9, 11*4),
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
    day = '24'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 10439961859
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 72050269
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
