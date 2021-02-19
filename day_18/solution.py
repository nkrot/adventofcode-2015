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


def parse_lines(lines: List[str]) -> List[List[int]]:
    board = []
    for line in lines:
        line = line.strip()
        board.append([1 if ch == '#' else 0 for ch in line])
    assert len(board) == len(board[0]), "Board musy be square"
    return board


def cells(brd):
    for r in range(len(brd)):
        for c in range(len(brd[r])):
            yield (r, c, brd[r][c])


def update(board, statechanger: Callable):
    shape = (len(board), len(board[0]))

    def neighbours_of(rc: Tuple[int, int], val=1):
        '''collect neighbours of given position <rc> that have value <val>'''
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),  (0, +1),
                   (+1, -1), (+1, 0), (+1, +1)]
        cells = []
        for dr, dc in offsets:
            nr, nc = rc[0] + dr, rc[1] + dc
            if 0 <= nr < shape[0] and 0 <= nc < shape[1]:
                if val is None or val == board[nr][nc]:
                    cells.append((nr, nc, board[nr][nc]))
        return cells

    newboard = [[0] * shape[1] for r in range(shape[0])]

    for cell in cells(board):
        r, c, state = cell
        # print(cell)
        newboard[r][c] = statechanger(cell, neighbours_of((r, c)), shape)

    return newboard


def count_lights_on(board):
    rows = map(sum, board)
    return sum(rows)


def solve_p1(lines: List[str], n_steps: int = 100) -> int:
    """Solution to the 1st part of the challenge"""
    board = parse_lines(lines)

    def compute_light_state(light, neighbours, *args):
        r, c, state = light
        c_neighbours_on = len(neighbours)
        newstate = 0
        if state == 1 and c_neighbours_on in (2, 3):
            # light stays on
            newstate = 1
        elif state == 0 and c_neighbours_on == 3:
            # light turns on
            newstate = 1
        return newstate

    for i in range(n_steps):
        board = update(board, compute_light_state)

    return count_lights_on(board)


def solve_p2(lines: List[str], n_steps: int = 100) -> int:
    """Solution to the 2nd part of the challenge"""

    board = parse_lines(lines)

    def compute_light_state(light, neighbours, shape):
        r, c, state = light
        c_neighbours_on = len(neighbours)
        newstate = 0
        corners = ((0, 0), (0, shape[1] - 1),
                   (shape[0] - 1, 0), (shape[0] - 1, shape[1] - 1))
        if (r, c) in corners:
            newstate = 1
        elif state == 1 and c_neighbours_on in (2, 3):
            # light stays on
            newstate = 1
        elif state == 0 and c_neighbours_on == 3:
            # light turns on
            newstate = 1
        return newstate

    for i in range(n_steps):
        board = update(board, compute_light_state)

    return count_lights_on(board)


text_1 = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####.."""


text_2 = """\
##.#.#
...##.
#....#
..#...
#.#..#
####.#"""


tests = [
    (text_1.split('\n'), 4, None),
    (text_2.split('\n'), None, 17),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp, 4)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp, 5)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '18'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 1061
    res1 = solve_p1(lines, 100)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 1006
    res2 = solve_p2(lines, 100)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
