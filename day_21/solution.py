#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Optional, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


class Player(object):

    def __init__(self, hit_points, damage, armor, name=None):
        self.hit_points = int(hit_points)
        self.damage = int(damage)
        self.armor = int(armor)
        self.name = name or 'You'

    def attacks(self, other: 'Player') -> None:
        other.accepts_attack(self)

    def accepts_attack(self, other: 'Player') -> None:
        self.hit_points -= max(1, other.damage - self.armor)

    @property
    def is_alive(self):
        return self.hit_points > 0

    def __repr__(self):
        return "<{}: [{}] hp={}, damage={}, armor={}>".format(
            self.__class__.__name__,
            self.name, self.hit_points, self.damage, self.armor)


class Boss(Player):
    def __init__(self, *args):
        if not(args):
            args = (100, 8, 2)  # data from input.txt
        super().__init__(*args, "Boss")


def play(pl_1, pl_2) -> Tuple[Player, int]:
    '''Runs a game between two players and returns the winner player
    and its index among the players'''
    while True:
        pl_1.attacks(pl_2)
        if not pl_2.is_alive:
            return pl_1, 0
        pl_2.attacks(pl_1)
        if not pl_1.is_alive:
            return pl_2, 1
    return None, None


def demo_1():
    print("Demo: A simple game")
    you = Player(8, 5, 5)
    boss = Boss(12, 7, 2)
    print("Player[0]:", you)
    print("Player[1]:", boss)
    winner, idx = play(you, boss)
    print("Won: {}, {}".format(idx, winner))

def demo_2():
    print("Demo:")
    pass


#demo_1()
demo_2()

# TODO
# - select possible configurations of player 1
#   a factory for generating warriors
# - which of the winning configutaions is the cheapest

exit(100)

def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    # TODO
    return 0


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


text_1 = """hello
yellow
melon"""

tests = [
    # (text_1.split('\n'), exp1, exp2),
    # TODO
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
    day = '21'
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
