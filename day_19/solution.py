#!/usr/bin/env python

# # #
# TODO: p2 not solved
#

import re
import os
import sys
from typing import List, Tuple, Dict
from collections import defaultdict, Counter

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def parse_lines(lines: List[str]) -> Tuple[Dict, str]:
    reactions = defaultdict(list)
    molecule = None
    for line in lines:
        line = line.strip()
        m = re.search(r'(\S+)\s+=>\s+(\S+)', line)
        if m:
            reactions[m.group(1)].append(m.group(2))
        elif line:
            molecule = line
    return reactions, molecule


def run_reactions(molecule: str, reactions):
    r = re.compile('({})'.format("|".join(set(reactions.keys()))))
    for m in r.finditer(molecule):
        st, ed = m.span()
        head, tail = molecule[:st], molecule[ed:]
        for repl in reactions[m[1]]:
            yield head + repl + tail


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    reactions, molecule = parse_lines(lines)
    # print(reactions)
    newmolecules = set(run_reactions(molecule, reactions))
    return len(newmolecules)


def solve_p2_v1(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge
    Breadth-First Search approach, terribly slow
    """
    reactions, target = parse_lines(lines)
    molecules = ['e']
    seen = dict()
    n_steps = 0
    found = False
    while not found:
        n_steps += 1
        n_tries = len(molecules)
        for i in range(n_tries):
            molecule = molecules.pop(0)
            print(n_steps, molecule)
            for newmolecule in run_reactions(molecule, reactions):
                if target == newmolecule:
                    found = True
                    break
                if newmolecule not in seen:
                    molecules.append(newmolecule)
                    seen[newmolecule] = 1
    return n_steps


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge
    """
    reactions, target = parse_lines(lines)
    seen = {}
    return fabricate('e', reactions, target, seen, 0)


def fabricate(curr_molecule: str,
              reactions: Dict[str, List],
              target_molecule: str,
              seen_molecules: Dict[str, int],
              depth: int):

    # print(depth, curr_molecule)

    if not has_chance(target_molecule, curr_molecule) and depth > 0:
        return None

    if curr_molecule == target_molecule:
        return depth

    if len(curr_molecule) >= len(target_molecule):
        # it does not make sense to continue
        return None

    depth += 1
    for new_molecule in run_reactions(curr_molecule, reactions):
        # print(curr_molecule, "-->", new_molecule)
        if new_molecule not in seen_molecules:
            # seen_molecules[new_molecule] = depth
            res = fabricate(new_molecule, reactions, target_molecule,
                            seen_molecules, depth)
            if res and res > 0:
                return res
    return None


def has_chance(target: str, current: str) -> bool:
    t = Counter(target)
    c = Counter(current)
    diff = (c - t) & t
    return len(diff) == 0


text_1 = """\
H => HO
H => OH
O => HH

HOH"""


text_2 = text_1.split('\n')[:-1] + ['HOHOHO']


text_3 = """\
e => H
e => O
H => HO
H => OH
O => HH

HOH"""


text_4 = text_3.split('\n')[:-1] + ['HOHOHO']


tests = [
    (text_1.split('\n'),
     len(set(["HOOH", "HOHO", "OHOH", "HOOH" "HHHH"])),
     None),
    (text_2, 7, None),
    (text_3.split('\n'), None, 3),
    (text_4, None, 6)
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
    day = '19'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 509
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    # print(f"--- Day {day} p.2 ---")
    # exp2 = -1
    # res2 = solve_p2(lines)
    # print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
