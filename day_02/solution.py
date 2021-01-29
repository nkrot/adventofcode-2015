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


def to_dims(line: str) -> List[int]:
    return [int(d) for d in line.strip().split('x')]


def amount_of_paper(dims: List[int]) -> int:
    assert len(dims) == 3, f"Wrong dimensions: {dims}"
    areas = [dims[0] * dims[1], dims[0] * dims[2], dims[1]*dims[2]]
    return (2 * sum(areas) + min(areas))


def volume(dims: List[int]) -> int:
    return reduce(lambda x, y: x*y, dims, 1)


def amount_of_ribbon(dims: List[int]) -> int:
    assert len(dims) == 3, f"Wrong dimensions: {dims}"
    perimeters = [2 * (dims[0] + dims[1]),
                  2 * (dims[0] + dims[2]),
                  2 * (dims[1] + dims[2])]
    return min(perimeters) + volume(dims)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    amounts = [amount_of_paper(to_dims(line)) for line in lines]
    return sum(amounts)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    amounts = [amount_of_ribbon(to_dims(line)) for line in lines]
    return sum(amounts)


tests = [
    ("2x3x4",  2*6 + 2*12 + 2*8 + 6, 2+2+3+3 + 2*3*4),
    ("1x1x10", 2*1 + 2*10 + 2*10 + 1, 1+1+1+1 + 1*1*10),
    ("2x3x4\n1x1x10", 58 + 43, 34+14)
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        inp = inp.split('\n')

        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '02'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 1598415
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 3812909
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
