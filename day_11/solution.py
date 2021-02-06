#!/usr/bin/env python

# # #
#
#

from typing import Union

DEBUG = False

# does not work with standard classes
# def open(klass):
#     def update(mixin):
#         for k, v in mixin.__dict__.items():
#             if k != '__dict__':
#                 setattr(klass, k, v)
#         return klass
#     return update


class Password(str):

    @classmethod
    def is_valid(cls, password: Union['Password', str]) -> bool:
        """
        Requirements for a password being valid:
        1) must include one increasing straight of at least three letters,
           like abc, bcd, cde, and so on, up to xyz.
           They cannot skip letters; abd doesn't count.
        2) may not contain the letters i, o, or l, as these letters can be
           mistaken for other characters and are therefore confusing.
        3) must contain at least two different, non-overlapping pairs of
           letters, like aa, bb, or zz.
        """
        # print('Password', cls, password)

        # Req. 2
        if not set(password).isdisjoint('iol'):
            return False
        # Req. 1
        codes = [ord(ch) for ch in password]
        straights = [c2-c1 == 1 and c3-c2 == 1
                     for c1, c2, c3 in zip(codes, codes[1:], codes[2:])]
        if True not in straights:
            return False
        # Req. 3
        dups = set(ch1 for ch1, ch2 in zip(password, password[1:])
                   if ch1 == ch2)
        return len(dups) > 1

    def incr(self):
        '''Increment password by one step'''
        codes = list(reversed([ord(ch) for ch in self]))
        for pos in range(len(codes)):
            codes[pos] += 1
            if codes[pos] > ord('z'):
                codes[pos] = ord('a')
            else:
                break
        s = "".join([chr(code) for code in reversed(codes)])
        return self.__class__(s)

    # def is_valid(self):
    #     raise PythonSucksError()


# s = Password('xx')
# for _ in range(5):
#     print(s)
#     s = s.incr()
# print(s)
# exit(100)


def solve_p1(s: str) -> str:
    """Solution to the 1st part of the challenge"""
    password = Password(s)
    while True:
        password = password.incr()
        if Password.is_valid(password):
            break
    return password


def solve_p2(password: str) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(solve_p1(password))


tests = [
    # tests for is_valid
    ('hijklmmn', None, None, False),
    ('abbceffg', None, None, False),
    ('abbcegjk', None, None, False),
    ('abcdffaa', None, None, True),
    ('ghjaabcc', None, None, True),

    # tests for generation of the next password
    ('abcdefgh', 'abcdffaa', None, None),
    ('ghijklmn', 'ghjaabcc', None, None),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2, exp3) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)

        if exp3 is not None:
            res3 = Password.is_valid(inp)
            print(f"T3.{tid}:", res3 == exp3, exp3, res3)


def run_real():
    day = '11'
    line = 'cqjxjnds'

    print(f"--- Day {day} p.1 ---")
    exp1 = 'cqjxxyzz'
    res1 = solve_p1(line)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 'cqkaabcc'
    res2 = solve_p2(line)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
