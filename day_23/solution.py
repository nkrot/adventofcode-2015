#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def parse_lines(lines: List[str]) -> Tuple[List, Dict]:
    instructions, registers = [], {}
    for line in lines:
        line = line.strip()
        if line:
            tokens = line.replace(',', '').split()
            if tokens[0] in ('jmp', 'jie', 'jio'):
                tokens[-1] = int(tokens[-1])
            instructions.append(tuple(tokens))
            if tokens[0] not in ('jmp',):
                registers[tokens[1]] = 0
    if DEBUG:
        print(registers)
        print(instructions)
    return instructions, registers


def execute(instructions, registers, pos):
    instr = instructions[pos]
    offset = 1

    if DEBUG:
        print(instr)

    if instr[0] == 'hlf':
        registers[instr[1]] /= 2
    elif instr[0] == 'tpl':
        registers[instr[1]] *= 3
    elif instr[0] == 'inc':
        registers[instr[1]] += 1
    elif instr[0] == 'jmp':
        offset = instr[1]
    elif instr[0] == 'jie':
        if registers[instr[1]] % 2 == 0:
            offset = instr[2]
    elif instr[0] == 'jio':
        if registers[instr[1]] == 1:
            offset = instr[2]

    if DEBUG:
        print(registers, offset)

    return pos + offset


def run(instructions, registers):
    pos = 0
    while pos < len(instructions):
        pos = execute(instructions, registers, pos)


def solve_p1(lines: List[str], regname="b") -> int:
    """Solution to the 1st part of the challenge"""
    instructions, registers = parse_lines(lines)
    run(instructions, registers)
    return registers[regname]


def solve_p2(lines: List[str], regname='b') -> int:
    """Solution to the 2nd part of the challenge"""
    instructions, registers = parse_lines(lines)
    registers['a'] = 1
    run(instructions, registers)
    return registers[regname]


text_1 = """\
inc a
jio a, +2
tpl a
inc a
"""


tests = [
    (text_1.split('\n'), 2, None),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp, "a")
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '23'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 307
    res1 = solve_p1(lines, "b")
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 160
    res2 = solve_p2(lines, "b")
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
