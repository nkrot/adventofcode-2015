#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Optional, Tuple
import itertools

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


class Player(object):

    @classmethod
    def with_armament(cls, weapons: List[Tuple]):
        obj = cls(100, 0, 0)
        obj.weapons = tuple(weapons)
        return obj

    def __init__(self, hit_points=100, damage=0, armor=0, name=None):
        self.hit_points = int(hit_points)
        self.damage = int(damage)
        self.armor = int(armor)
        self.name = name or 'You'
        self._weapons = None

    @property
    def weapons(self):
        return self._weapons

    @weapons.setter
    def weapons(self, items: List[Tuple]):
        self._weapons = tuple(filter(len, items))
        self.damage = 0
        self.armor = 0
        for _, cost, damage, armor in self._weapons:
            self.damage += damage
            self.armor += armor

    def attacks(self, other: 'Player') -> None:
        other.accepts_attack(self)

    def accepts_attack(self, other: 'Player') -> None:
        self.hit_points -= max(1, other.damage - self.armor)

    @property
    def is_alive(self):
        return self.hit_points > 0

    def __repr__(self):
        return "<{}: [{}] hp={}, damage={}, armor={}; weapon={}>".format(
            self.__class__.__name__,
            self.name, self.hit_points, self.damage, self.armor,
            self.weapons)


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

weapons = [
    # (Name, Cost  Damage  Armor)
    ("Dagger",      8, 4, 0),
    ("Shortsword", 10, 5, 0),
    ("Warhammer",  25, 6, 0),
    ("Longsword",  40, 7, 0),
    ("Greataxe",   74, 8, 0)
]

armors = [
    # Name, Cost  Damage  Armor
    ("Leather",     13, 0, 1),
    ("Chainmail",   31, 0, 2),
    ("Splintmail",  53, 0, 3),
    ("Bandedmail",  75, 0, 4),
    ("Platemail",  102, 0, 5),
]

rings = [
    # Name, Cost  Damage  Armor
    ("Damage +1",   25, 1, 0),
    ("Damage +2",   50, 2, 0),
    ("Damage +3",  100, 3, 0),
    ("Defense +1",  20, 0, 1),
    ("Defense +2",  40, 0, 2),
    ("Defense +3",  80, 0, 3),
]

def cost_of_weapons(weapons: List[Tuple]) -> int:
    return sum(w[1] for w in weapons)

def combinations_of_weapons():
    '''Generate allowed combinations of weapons, armors and rings
    * weapons: 1
    * armors:  0 or 1
    * rings:   0 or 1 or 2
    The shop only has one of each item, so you can't buy, for example,
    two rings of Damage +3.
    '''
    # TODO: there must be a nicer way to do it
    _weapons = weapons
    _armors = [()] + armors
    _rings = [[()]] + [[r] for r in rings] + list(itertools.combinations(rings, 2))
    for cmb in itertools.product(_weapons, _armors, _rings):
        yield(list(cmb[0:2]) + list(cmb[2][:]))
    return []


def demo_1():
    print("-- Demo: A simple game ---" )
    you = Player(8, 5, 5)
    boss = Boss(12, 7, 2)
    print("Player[0]:", you)
    print("Player[1]:", boss)
    winner, idx = play(you, boss)
    print("Won: {}, {}".format(idx, winner))

def demo_2():
    print("--- Demo: An armed Player ---")
    equipment = weapons[:2] + armors[:1] + rings[1:2]
    you = Player.with_armament(equipment)
    print("Player[0]:", you)


def demo_3():
    print("--- Demo: Allowed combinations of armament ---")
    for idx, armaments in enumerate(combinations_of_weapons()):
        print(idx, armaments)
        pl = Player.with_armament(armaments)
        print(pl)
        print("Cost of armament:", cost_of_weapons(pl.weapons))
        print()


#demo_1()
#demo_2()
#demo_3()


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    cost = cost_of_weapons(weapons + armors + rings)
    for armaments in combinations_of_weapons():
        you = Player.with_armament(armaments)
        winner, idx = play(you, Boss())
        if idx == 0:  # player won
            cost = min(cost, cost_of_weapons(winner.weapons))
    return cost


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
    exp1 = 91
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = -1
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    # run_tests()
    run_real()
