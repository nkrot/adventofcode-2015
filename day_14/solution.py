#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Dict, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def parse_lines(lines: List[str]) -> Dict[str, Tuple[int, int, int]]:
    cars = {}
    for line in lines:
        fields = line.strip().split()
        if fields:
            cars[fields[0]] = (int(fields[3]), int(fields[6]), int(fields[-2]))
    return cars


def travel_distance(params, time):
    speed, t_move, t_rest = params

    t_burst = t_move + t_rest
    nb = time // t_burst
    d1 = speed * t_move * nb

    # t2 = min(time - (nb * t_burst), t_move)
    t2 = min(time % t_burst, t_move)
    d2 = speed * t2

    return d1 + d2


def solve_p1(lines: List[str], nsec: int) -> int:
    """Solution to the 1st part of the challenge"""
    deer = parse_lines(lines)

    if DEBUG:
        print(deer)

    distances = {name: travel_distance(params, nsec)
                 for name, params in deer.items()}

    if DEBUG:
        print(distances)

    return max(distances.values())


def solve_p2(lines: List[str], nsec: int) -> int:
    """Solution to the 2nd part of the challenge"""
    deer = parse_lines(lines)
    points = {name: 0 for name in deer.keys()}
    for t in range(1, 1+nsec):
        if DEBUG:
            print("Time tick", t)
        distances = {name: travel_distance(params, t)
                     for name, params in deer.items()}
        maxd = max(distances.values())

        if DEBUG:
            print("..Distances", distances)
            print("..max distance:", maxd)

        winners = []
        for name in points:
            if distances[name] == maxd:
                points[name] += 1
                winners.append(name)
        if DEBUG:
            print("..Winner(s):", ", ".join(winners))

    if DEBUG:
        print("Points", points)

    return max(points.values())


text_1 = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""


tests = [
    (text_1.split('\n'), (11, 176), (140, 139)),
    (text_1.split('\n'), (1000, 1120), (1000, 689)),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, (nsec1, exp1), (nsec2, exp2)) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp, nsec1)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp, nsec2)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '14'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 2660
    res1 = solve_p1(lines, 2503)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 1256
    res2 = solve_p2(lines, 2503)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
