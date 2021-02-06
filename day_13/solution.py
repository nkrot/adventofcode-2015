#!/usr/bin/env python

# # #
# Based on day 08 solution.
# NP-hard approach.
#

import os
import sys
from typing import List, Tuple, Dict
from itertools import permutations

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def parse_lines(lines: List[str]) -> (Dict[Tuple[str, str], int], Tuple[str]):
    manas, attendees = {}, set()
    signs = {'gain': +1, 'lose': -1}
    for line in lines:
        fields = line.strip('.\n').split()
        if fields:
            a1, a2 = fields[0], fields[-1]
            manas[(a1, a2)] = signs[fields[2]] * int(fields[3])
            attendees.update((a1, a2))
    return manas, tuple(attendees)


def compute_happiness(sitting: tuple, manas: dict) -> int:
    sitting = list(sitting) + [sitting[0]]
    total = 0
    for g1, g2 in zip(sitting, sitting[1:]):
        total += manas.get((g1, g2), 0)
        total += manas.get((g2, g1), 0)
    return total


def solve_p1(lines: List[str], part2=False) -> int:
    """Solution to the 1st part of the challenge"""
    manas, guests = parse_lines(lines)
    if part2:
        guests = tuple(list(guests) + ['myself'])
    sitting_arrangements = permutations(guests)
    happiness_levels = [compute_happiness(sa, manas)
                        for sa in sitting_arrangements]
    return max(happiness_levels)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, True)


text_1 = """
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""


tests = [
    (text_1.split('\n'), 330, None),
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
    day = '13'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 618
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 601
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
