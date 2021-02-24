#!/usr/bin/env python

# # #
#
# managed to do p2 exclusively thanks to
# https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/
#
# TODO:
# 1. why replacing righmost before leftmost works?


import re
import os
import sys
from typing import List, Tuple, Dict
from collections import defaultdict, Counter

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = not False


def parse_lines(lines: List[str], rev: bool = False) -> Tuple[Dict, str]:
    reactions = defaultdict(list)
    molecule = None
    for line in lines:
        line = line.strip()
        m = re.search(r'(\S+)\s+=>\s+(\S+)', line)
        if m:
            a, b = (2, 1) if rev else (1, 2)
            reactions[m.group(a)].append(m.group(b))
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


def fabricate(curr_molecule: str,
              reactions: Dict[str, List],
              target_molecule: str,
              seen_molecules: Dict[str, int],
              depth: int):
    '''this shit is terribly slow'''
    print(depth, curr_molecule)

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
    '''it does improve performance a bit but still too slow'''
    t = Counter(target)
    c = Counter(current)
    diff = (c - t) & t
    return len(diff) == 0


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


def solve_p2_v2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge
    Depth-First recursive approach.
    Very slow. Not sure if it completes.
    """
    reactions, target = parse_lines(lines)
    seen = {}
    return fabricate('e', reactions, target, seen, 0)


def solve_p2_v3(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge.
    This algorithm works in the opposite direction: starts with final
    molecule and applies reversed replacements to convert it to
    the initial state.
    Again, it will generate *all* possible ways to reduce the molecule,
    which is an overkill.

    While this works for tests, it will take very long for longer
    mocules like the one in input.txt.
    """
    reactions, molecule = parse_lines(lines, True)
    cnt = 0
    molecules = [molecule]
    while molecules:
        cnt += 1
        for _ in range(len(molecules)):
            curr = molecules.pop(0)
            if DEBUG:
                print(f'Starting {cnt}: {curr}, other {molecules}')
            for newmolecule in run_reactions(curr, reactions):
                if newmolecule not in molecules:
                    if DEBUG:
                        print("  -->", newmolecule)
                    if set(newmolecule) == set('e'):
                        # TODO: by some reason, T2.0 (text_3) is reduced to
                        # more than one 'e'
                        return cnt
                    molecules.append(newmolecule)
    print(cnt)
    return None


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge.
    This algorithm works in the opposite direction: starts with final
    molecule and applies replacements from right to left to convert it to
    the initial state (reducing the input).
    """
    reactions, molecule = parse_lines(lines, True)

    assert set(map(len, reactions.values())) == set([1]), \
        "Ambiguous replacements. This solution is not applicable."

    # reverse the strings.
    # By some reason, it works iff rightmost occurrences are replaced first
    # TODO: why????
    reactions = {k[::-1]: vs[0][::-1] for k, vs in reactions.items()}
    molecule = molecule[::-1]

    r = re.compile('({})'.format("|".join(set(reactions.keys()))))

    cnt = 0
    while set(molecule) != {'e'}:
        m = re.search(r, molecule)
        if m:
            cnt += 1
            st, ed = m.span()
            molecule = molecule[:st] + reactions[m[1]] + molecule[ed:]
        else:
            # the algorithm did not complete
            cnt = 0
            break
    return cnt


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
    # (text_1.split('\n'),
    #  len(set(["HOOH", "HOHO", "OHOH", "HOOH" "HHHH"])),
    #  None),
    # (text_2, 7, None),
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

    print(f"--- Day {day} p.2 ---")
    exp2 = 195
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
