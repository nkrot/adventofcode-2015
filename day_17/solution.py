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


def combinations(items: List[int], target: int):
    if target == 0:
        yield ()
    else:
        for i in range(len(items)):
            for comb in combinations(items[i+1:], target-items[i]):
                yield (items[i],) + comb


def solve_p1(lines: List[str], total: int) -> int:
    """Solution to the 1st part of the challenge"""
    containers = [int(ln) for ln in lines if ln]
    if DEBUG:
        print(containers)
    selected = list(combinations(containers, total))
    if DEBUG:
        for comb in selected:
            print(comb)
    return len(selected)


def solve_p2(lines: List[str], total: int) -> int:
    """Solution to the 2nd part of the challenge"""
    containers = [int(ln) for ln in lines if ln]
    counts = list(map(len, combinations(containers, total)))
    # print(list(counts))
    return counts.count(min(counts))


text_1 = """\
20
15
10
5
5"""


tests = [
    (text_1.split('\n'),
     len([(15, 10), (20, 5), (20, 5), (15, 5, 5)]), 3),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp, 25)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp, 25)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '17'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 1304
    res1 = solve_p1(lines, 150)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 18
    res2 = solve_p2(lines, 150)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
