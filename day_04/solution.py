#!/usr/bin/env python

# # #
#
#

import hashlib


DEBUG = False


def solve_p1(head: str, prefix='00000') -> int:
    """Solution to the 1st part of the challenge"""
    for tail in range(10**len(head)):
        s = '{}{}'.format(head, tail)
        digest = hashlib.md5(bytes(s, 'utf-8')).hexdigest()
        if digest.startswith(prefix):
            return tail
    return None


def solve_p2(head: str) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(head, '000000')


tests = [
    ('abcdef',  609043, None),
    ('pqrstuv', 1048970, None),
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
    day = '04'
    inp = 'ckczppom'

    print(f"--- Day {day} p.1 ---")
    exp1 = 117946
    res1 = solve_p1(inp)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 3938038
    res2 = solve_p2(inp)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
