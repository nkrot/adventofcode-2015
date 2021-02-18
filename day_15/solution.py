#!/usr/bin/env python

# # #
# This solution implement brute force algorithm that can be made better.
# Especially part 2 should be easy to optimize.
# Is DP applicable?
#

import re
import os
import sys
from typing import List
from functools import reduce

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


class Ingredient(object):
    @classmethod
    def from_line(cls, text: str):
        text = re.sub('[:,]', '', text.strip())
        fields = text.split()
        obj = cls()
        obj.name = fields.pop(0)
        obj.properties = tuple(fields[0::2])
        obj.values = tuple(map(int, fields[1::2]))
        return obj

    def __init__(self):
        self.name = None
        self.properties = None  # propery names
        self.values = None      # property values

    @property
    def calories(self):
        return self.values[-1]

    def __mul__(self, k: int):
        obj = self.__class__()
        obj.name = str(self.name)
        obj.properties = tuple(self.properties)
        obj.values = tuple(map(lambda v: v*k, self.values))
        return obj

    def __rmul__(self, k: int):
        return self * k

    def __add__(self, other):
        if other == 0:
            # to support sum(List[Ingredient]), need to implement
            #   0 + Ingredient
            obj = self
        else:
            obj = self.__class__()
            obj.name = 'Composition'
            obj.properties = tuple(self.properties)
            obj.values = tuple(map(lambda vs: sum(vs),
                                   zip(self.values, other.values)))
        return obj

    def __radd__(self, other):
        '''For simmetry and also for making work sum(List[Ingredient])'''
        return self + other

    def score(self):
        '''Consider all properties except calories'''
        values = [max(v, 0) for v in self.values[0:4]]
        return reduce(lambda x, y: x*y, values, 1)

    def __repr__(self):
        return "<{}: name={}, prop-values={}, prop-names: {}>".format(
            self.__class__.__name__, self.name, self.values, self.properties)


def parse_lines(lines: List[str]):
    ingrs = []
    for line in lines:
        if ':' in line:
            ingrs.append(Ingredient.from_line(line))
    return ingrs


def gen_amounts(n, total=100):
    '''Generate all possible combinations on <n> numbers that
    sum up to <total>'''
    if n < 1:
        raise ValueError('impossible')
    elif n == 1:
        yield (total,)
    else:
        for f in range(total+1):
            for prm in gen_amounts(n-1, total-f):
                yield (f,) + prm


def make_cookie(amounts: List[int], ingredients: List[Ingredient]):
    '''Make a cookie by mixing given ingredients in given amounts'''
    return sum(map(lambda vs: vs[0]*vs[1], zip(amounts, ingredients)))


def solve_p1(lines: List[str], max_calories=None) -> int:
    """Solution to the 1st part of the challenge"""
    ingrs = parse_lines(lines)

    # TODO: this is a terrible brute force algorithm
    max_score = -1
    for amounts in gen_amounts(len(ingrs), 100):
        cookie = make_cookie(amounts, ingrs)
        if not max_calories or cookie.calories == max_calories:
            max_score = max(cookie.score(), max_score)

    return max_score


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, 500)


text_1 = """
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
"""


tests = [
    (text_1.split('\n'), 68 * 80 * 152 * 76, 57600000),
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
    day = '15'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 21367368
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 1766400
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
