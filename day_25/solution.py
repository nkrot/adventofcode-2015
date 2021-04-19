#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import Tuple


DEBUG = False


def compute_number_at(pos: Tuple[int, int]) -> int:
    r, c = pos
    pdiag = r + c - 2  # previous diagonal
    # The factorial with summation is "triangular number"
    n_steps = int((pdiag * pdiag + pdiag) / 2 + c)

    prev = 20151125
    for s in range(n_steps-1):
        prev = prev * 252533 % 33554393
        # print(2+s, prev)

    return prev


def solve_p1(pos: Tuple[int, int]) -> int:
    """Solution to the 1st part of the challenge"""
    return compute_number_at(pos)


def solve_p2(pos: Tuple[int, int]) -> int:
    """Solution to the 2nd part of the challenge.
    There is no part 2 in this day.
    """
    return -1


tests = [
    ((2, 3), 16929656, None),
    ((5, 2), 17552253, None),
    ((6, 2), 6796745, None)
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
    day = '25'
    inp = (2978, 3083)

    print(f"--- Day {day} p.1 ---")
    exp1 = 2650453
    res1 = solve_p1(inp)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    print("No task is provided, the star is granted.")
    # exp2 = -1
    # res2 = solve_p2(inp)
    # print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
