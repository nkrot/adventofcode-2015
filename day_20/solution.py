#!/usr/bin/env python

# # #
# TODO
# 1) what is Robbin's theorem?
# 2) find all divisors based on prime numbers
#     http://www.cleverstudents.ru/divisibility/all_divisors_of_number.html
# 3) measure runtime of some solutions


import math


DEBUG = False


class DeliveryService(object):

    def __init__(self):
        self.last_visited_house = None

    def visit(self, house: int) -> int:
        '''return number of presents delivered to this house'''
        n_presents = 0
        self.last_visited_house = house
        # houses = []
        for h in range(1, 1+self.last_visited_house):
            if house % h == 0:
                # n_presents += h
                n_presents += 10*h
                # houses.append(i)
        # print(houses, n_presents)
        return n_presents


def solve_p1_v1(target: int) -> int:
    """This solution is super slow, runs 3+ hrs on gpu machine"""

    elves = DeliveryService()

    house, n_presents = 0, 0
    while n_presents < target:
        house += 1
        n_presents = elves.visit(house)
        print(house, n_presents)

    return house


def solve_p1_v2(target: int) -> int:
    """This solution is a feractoring of solve_p1_v1(), it saves time
    on function called.
    Performance is on par with solve_p1_v1()
    """
    house, n_presents = 0, 0
    while n_presents < target:
        house += 1
        n_presents = 0
        for elf in range(1, 1+house):
            if house % elf == 0:
                n_presents += 10*elf
        if DEBUG and house % 10000 == 0:
            print(f"House: {house} got {n_presents}")
    return house


def solve_p1_v3(target: int) -> int:
    """Optimization of the parts in solve_p1_v2() that computes divisors of
    a number:
    n=20: 1, 2, 4, 5, 10, 20
    - divisors come in pairs (d, D): (1, 20), (2, 10), (4, 5).
      when d is found, D is also found
    - the value of d is no larger than sqrt(n). any numbers larger than sqrt(n)
      will produce pairs (D, d).

    Performance: this completes in under a minute.
    """
    house, n_presents = 0, 0
    while n_presents < target:
        house += 1
        n_presents = 0
        for elf in range(1, 1+int(math.sqrt(house))):
            if house % elf == 0:
                n_presents += 10 * elf
                other = house/elf
                if elf != other:
                    n_presents += 10 * int(other)
        if DEBUG and house % 10000 == 0:
            print(f"House: {house} got {n_presents}")
    return house


def solve_p1_v5(target: int) -> int:
    '''This solution uses much memory but runs must faster than solve_p1_v1'''
    mh = 1 + int(target / 10)
    npresents = [10] * mh
    for elf in range(2, mh):
        for h in range(elf, mh, elf):
            npresents[h] += 10*elf
    if DEBUG:
        print(target, [(i, n) for i, n in enumerate(npresents)])
    for h, np in enumerate(npresents):
        if np >= target:
            return h
    return -1


def solve_p1(target: int) -> int:
    # return solve_p1_v1(target) # super slow, overengineering
    # return solve_p1_v2(target) # super slow
    return solve_p1_v3(target)   # fast
    # return solve_p1_v5(target) # fast, memory consuming


def solve_p2(target: int) -> int:
    """Solution to the 2nd part of the challenge"""
    mh = 1 + int(target / 10)
    npresents = [0] * mh
    for elf in range(1, mh):
        for h in range(elf, min(mh, elf*50), elf):
            npresents[h] += 11*elf
    if DEBUG:
        print(target, [(i, n) for i, n in enumerate(npresents)])
    for h, np in enumerate(npresents):
        if np >= target:
            return h
    return -1


tests = [
    (80,    6, None),
    (120,   6, None),
    (130,   8, None),
    (150,   8, None),
    (180,  10, None),
    (280,  12, None),
    (800,  36, None),
    (1200, 48, None),
    (1500, 60, None),
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
    day = '20'
    inp = 33100000

    print(f"--- Day {day} p.1 ---")
    exp1 = 776160
    res1 = solve_p1(inp)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 786240
    res2 = solve_p2(inp)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
