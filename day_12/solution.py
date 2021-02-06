#!/usr/bin/env python

# # #
#
#

import json


DEBUG = False


def sum_numbers(d, ignored=[]):
    s = 0
    if isinstance(d, dict):
        if not any(v in ignored for v in d.values()):
            for v in d.values():
                s += sum_numbers(v, ignored)
    elif isinstance(d, list):
        for v in d:
            s += sum_numbers(v, ignored)
    elif isinstance(d, int):
        s += d
    elif isinstance(d, str):
        pass
    else:
        raise AssertionError('Unrecognized obj type', type(d), d)
    return s


def solve_p1(string: str) -> int:
    """Solution to the 1st part of the challenge"""
    return sum_numbers(json.loads(string))


def solve_p2(string: str) -> int:
    """Solution to the 2nd part of the challenge"""
    return sum_numbers(json.loads(string), ['red'])


tests = [
    ('[1,2,3]', 6, 6),
    ('{"a":2,"b":4}', 6, None),
    ('{"a":[-1,1]}', 0, None),
    ('[-1,{"a":1}]', 0, None),
    ('[1,"red",5]', 6, 6),
    ('[1,{"c":"red","b":2},3]', None, 4),
    ('{"d":"red","e":[1,2,3,4],"f":5}', None, 0)
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
    day = '12'
    line = open('input.txt', 'r').read()

    print(f"--- Day {day} p.1 ---")
    exp1 = 156366
    res1 = solve_p1(line)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 96852
    res2 = solve_p2(line)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
