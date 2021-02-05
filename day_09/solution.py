#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List, Tuple, Dict
from itertools import permutations

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def parse_lines(lines: List[str]) -> (Dict[Tuple[str, str], int], Tuple[str]):
    distances, cities = {}, set()
    for line in lines:
        fields = line.strip().split()
        distances[(fields[0], fields[2])] = int(fields[4])
        cities.update((fields[0], fields[2]))
    return distances, tuple(cities)


def route_distance(route: tuple, distances: dict) -> int:
    # print('ROUTE', route)
    d = 0
    for i in range(1, len(route)):
        c1, c2 = route[i-1], route[i]
        d += distances.get((c1, c2), distances.get((c2, c1)))
    return d


def solve_p1(lines: List[str], part2=False) -> int:
    """Solution to the 1st part of the challenge"""
    distances, cities = parse_lines(lines)
    routes = permutations(cities)
    route_lengths = [route_distance(r, distances) for r in routes]
    if part2:
        res = route_lengths
    else:
        res = min(route_lengths)
    return res


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    lengths = solve_p1(lines, True)
    return max(lengths)


text_1 = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""


tests = [
    (text_1.split('\n'), 605, 982),
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
    day = '09'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 141
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 736
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
