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


def to_chars(line: str, unquote=True):
    chars = []
    # print(f"LINE: {line}")
    for m in re.finditer(r'(\\x[0-9a-f][0-9a-f]|\\.|.)', line):
        # print(m)
        chars.append(m.group(0))
    if unquote:
        chars = chars[1:-1]
    # print(chars)
    return chars


def escape_chars(chars: List[str]) -> List[str]:
    escaped = []
    for ch in chars:
        if ch.startswith('\\x') or ch in ("'", '"'):
            ch = '\\' + ch
        elif ch.startswith('\\'):
            ch = '\\' + '\\' + ch
        escaped.append(ch)
    return escaped


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    # print(lines)
    cnt_1 = sum([len(line) for line in lines])
    cnt_2 = sum([len(to_chars(line)) for line in lines])
    return cnt_1 - cnt_2


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    cnt_1, cnt_2 = 0, 0
    for line in lines:
        cnt_1 += len(line)
        chars = escape_chars(to_chars(line, False))
        s = "".join(chars)
        cnt_2 += len(s)
        cnt_2 += 2  # for additional surrounding quotes
    return cnt_2 - cnt_1


text_1 = utils.load_input('test.txt')


tests = [
    (text_1,
     (2 + 5 + 10 + 6) - (0 + 3 + 7 + 1),
     (6 + 9 + 16 + 11) - (2 + 5 + 10 + 6)),
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
    day = '08'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 1350
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 2085
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
