#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple, Callable

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def between(a, b):
    for x in range(a[0], b[0]+1):
        for y in range(a[1], b[1]+1):
            yield((x, y))


def parse(lines: List[str]) -> List[tuple]:
    commands = []
    for line in lines:
        line = line.strip()
        m = re.search(r'(\S+)\s(\d+),(\d+) through (\d+),(\d+)', line)
        if m:
            a = (int(m.group(2)), int(m.group(3)))
            b = (int(m.group(4)), int(m.group(5)))
            cmd = (m.group(1), a, b)
            commands.append(cmd)
        else:
            raise ValueError(f'Cannot parse {line}')
    return commands


def update_p1(lights: dict, light: Tuple[int, int], inst: str):
    if inst == 'on':
        lights[light] = 1
    elif inst == 'off':
        lights[light] = 0
    elif inst == 'toggle':
        if light not in lights:
            lights[light] = 1
        else:
            lights[light] = 1 - lights[light]
    else:
        raise ValueError(inst)


def update_p2(lights: dict, light: Tuple[int, int], inst: str):
    if inst == 'on':
        lights[light] = lights.get(light, 0) + 1
    elif inst == 'off':
        lights[light] = max(0, lights.get(light, 0) - 1)
    elif inst == 'toggle':
        lights[light] = lights.get(light, 0) + 2
    else:
        raise ValueError(inst)


def solve(lines: List[str], update: Callable) -> int:
    commands = parse(lines)
    lights = {}
    for (name, a, b) in commands:
        for light in between(a, b):
            update(lights, light, name)
    return sum(lights.values())


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    return solve(lines, update_p1)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve(lines, update_p2)


tests = [
    ('turn on 0,0 through 999,999', 1000000, None),
    ('toggle 0,0 through 999,0',    1000, None),
    # ('turn off 499,499 through 500,500', 4, None)

    ('turn on 0,0 through 0,0',    None, 1),
    ('toggle 0,0 through 999,999', None, 2000000)
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        inp = [inp]

        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '06'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 400410
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 15343601
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
