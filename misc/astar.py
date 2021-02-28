#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False
Coord = Tuple[int, int]


class Board(object):

    AROUND = (
        (-1, -1), (-1, 0), (-1, +1),
        ( 0, -1),          ( 0, +1),
        (+1, -1), (+1, 0), (+1, +1)
    )

    @classmethod
    def from_lines(cls, lines: List[str]):
        lines = [ln.strip() for ln in lines if ln]
        cells = {}
        for ri, row in enumerate(lines):
            for ci, col in enumerate(list(row)):
                cells[(ri,ci)] = col
        return cls(cells)

    def __init__(self, cells):
        self.cells = cells
        self.dims = [max(idxs) for idxs in zip(*self.cells.keys())]
        for xy, val in self.cells.items():
            if val == 'S':
                self.source = xy
            elif val == 'E':
                self.target = xy

    @property
    def shape(self):
        return tuple(self.dims)

    @property
    def height(self):
        return self.dims[0]

    @property
    def width(self):
        return self.dims[1]

    def __getitem__(self, xy: Coord):
        x, y = xy
        if 0 <= x < self.height and 0 <= y < self.width:
            return self.cells[xy]
        return None

    def __str__(self):
        lines = []
        for h in range(self.height):
            line = "".join([self.cells[h, w] for w in range(self.width)])
            lines.append(line)
        return "\n".join(lines)

    def distance(self, p1: Coord, p2: Coord):
        x1, y1 = p1
        x2, y2 = p2
        # d = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        d = abs(x2 - x1) + abs(y2 - y1)
        return d

    def adjacent(self, xy: Coord):
        x, y = xy
        for dx, dy in self.AROUND:
            nx, ny = x + dx, y + dy
            val = self[nx, ny]
            if val:
                yield (nx, ny), val


def demo(board):
    '''Demo some functionality of the board'''
    print(board)

    print("Dimensions", board.shape)
    print("Source", board.source, board[board.source])
    print("Target", board.target, board[board.target])

    pairs = [
        ((0,0), (1,1)),
        ((0,0), (1,0)),
        (board.source, board.target),
        (board.target, board.source)
    ]
    for p1, p2 in pairs:
        print("Distance between {} and {} is {}".format(
            p1, p2, board.distance(p1, p2)))

    points = [board.source, (5, 2)]
    for c in points:
        print("Points around", c)
        for p in board.adjacent(c):
            print(p)


def astar(board, s, t):
    print("Find path between:", s, t)

    # f(x) = g(x) + h(x)
    # g(x) - distance from the source to the current point
    # h(x) - distance from the current point to the target

    # each visited cell must record its coordinate and distances g(x), h(x), f(x)
    # it should be possible to find a visited cell by coordinate in the list of
    # visited cells
    # &&&

def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    board = Board.from_lines(lines)
    demo(board)
    astar(board, board.source, board.target)
    return 0


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


text_1 = """
..............
..x...........
..x...E.......
..x...........
..x...........
..xxxxxxxxxx..
..............
.....S........
..............
..............
"""


tests = [
    (text_1.split('\n'), True, None),
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
    day = 'DD'  # TODO
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = -1
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = -1
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    # run_real()
