#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple, Dict
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False

offsets = {
    '^': (-1, 0),  # northwards
    'v': (+1, 0),  # southwards
    '>': (0, +1),  # eastwards
    '<': (0, -1)   # westwards
}


def step(pos: Tuple[int, int], instruction: str):
    """Origin (0,0) if top left corner"""
    dx, dy = offsets[instruction]
    return (pos[0] + dx, pos[1] + dy)


def walk(pos: Tuple[int, int], route: List[str]) -> Dict[Tuple[int, int], int]:
    visited = defaultdict(int)
    visited[pos] = 1
    for inst in route:
        pos = step(pos, inst)
        visited[pos] += 1
    return visited


def solve_p1(line: str) -> int:
    """Solution to the 1st part of the challenge"""
    origin = (0, 0)
    houses = walk(origin, list(line))
    return len(houses)


def solve_p2(line: str) -> int:
    """Solution to the 2nd part of the challenge"""
    origin = (0, 0)
    santa_houses = walk(origin, line[0::2])
    robot_houses = walk(origin, line[1::2])
    return len(set(list(santa_houses.keys()) + list(robot_houses.keys())))


tests = [
    ('>',          2,    None),
    ('^v',         None, 3   ),
    ('^>v<',       4,    3   ),
    ('^v^v^v^v^v', 2,    11  )
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
    day = '03'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 2565
    res1 = solve_p1(lines[0])
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 2639
    res2 = solve_p2(lines[0])
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
