#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Optional, Callable

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


class AuntSue(object):

    @classmethod
    def from_line(cls, line: str):
        '''
        Sue 8: akitas: 10, vizslas: 9, children: 3
        '''
        tokens = re.sub(r'[:,]', '', line).split()
        properties = tokens[2::2]
        values = [int(v) for v in tokens[3::2]]
        obj = cls(int(tokens[1]), properties, values)
        # print(obj)
        return obj

    def __init__(self, id: int, properties: List[str], values: List[int]):
        self.id = id
        self.properties = tuple(properties)
        self.values = tuple(values)

    def __repr__(self):
        return "<{}: id={}, prop-vals={}>".format(
            self.__class__.__name__, self.id,
            list(zip(self.properties, self.values)))

    def value(self, propname: str) -> Optional[int]:
        try:
            idx = self.properties.index(propname)
            return self.values[idx]
        except ValueError:
            pass
        return None

    # def matches(self, profile: 'AuntSue') -> bool:


def match_p1(profile, aunt):
    """Test whether current AuntSue matches given profile.
    A perfect match is when the properies and their values of the current
    AuntSue match exactly corresponding properties and values of
    the profile.
    """
    matches = [pv == profile.value(pn)
               for pn, pv in zip(aunt.properties, aunt.values)]
    return all(matches)


def match_p2(profile, aunt):
    matches = []
    for an, av in zip(aunt.properties, aunt.values):
        pv = profile.value(an)
        if an in ('cats', 'trees'):
            ok = av > pv
        elif an in ('pomeranians', 'goldfish'):
            ok = av < pv
        else:
            ok = av == pv
        matches.append(ok)
    return all(matches)


def parse_lines(lines: List[str]) -> List[AuntSue]:
    aunts = []
    for line in lines:
        line = line.strip()
        if ':' in line:
            aunts.append(AuntSue.from_line(line))
    return aunts


def solve_p1(lines: List[str],
             profile: AuntSue,
             matcher: Callable = None) -> int:
    """Solution to the 1st part of the challenge"""
    matcher = matcher or match_p1
    aunts = parse_lines(lines)
    matching_aunts = [aunt for aunt in aunts if matcher(profile, aunt)]
    assert len(matching_aunts) == 1, "Expecting one solution only"
    return matching_aunts[0].id


def solve_p2(lines: List[str], profile: AuntSue) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, profile, match_p2)


text_1 = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""


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
    day = '16'
    lines = utils.load_input()
    profile = AuntSue.from_line(" ".join(['Sue -1'] + text_1.split('\n')))

    print(f"--- Day {day} p.1 ---")
    exp1 = 103
    res1 = solve_p1(lines, profile)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 405
    res2 = solve_p2(lines, profile)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    # run_tests()
    run_real()
