#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


class Gate(object):

    OPERATORS = {
        'INT'    : (1, '__int__'),
        'NOT'    : (1, '__invert__'),
        'AND'    : (2, '__and__'),
        'OR'     : (2, '__or__'),
        'LSHIFT' : (2, '__lshift__'),
        'RSHIFT' : (2, '__rshift__')
    }

    @classmethod
    def from_line(cls, line: str):
        """
        lx -> a
        0 -> c

        NOT kt -> ku

        hf AND hl -> hn
        he RSHIFT 5 -> hh
        """

        fields = line.split()
        assert len(fields) in [3, 4, 5], \
            f"Wrong number of fields: {len(fields)}"
        assert fields[-2] == '->', \
            f"Unrecognized line: {line}"

        gate = cls()
        gate.name = fields.pop()
        fields.pop()

        if DEBUG:
            print("Parsing", fields)

        if len(fields) == 2:
            gate.operator = fields.pop(0)
        elif len(fields) == 3:
            gate.operator = fields.pop(1)

        gate.operands = fields

        return gate

    def __init__(self):
        self.name = None
        self.operator = 'INT'
        self._operands = None
        self.circuit = None
        self._signal = None

    def connect_to(self, circuit: dict):
        circuit[self.name] = self
        self.circuit = circuit

    def reset(self):
        self._signal = None

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, op):
        assert op in self.OPERATORS, f"Unrecognized operation '{op}'"
        self._operator = op

    @property
    def operands(self):
        return self._operands

    @operands.setter
    def operands(self, vals):
        self._operands = [int(v) if re.match(r'\d+', v) else v for v in vals]

    @property
    def signal(self):
        if self._signal is None:
            self.execute()
        return self._signal

    @signal.setter
    def signal(self, value):
        self._signal = value

    def execute(self):
        arity, meth = self.OPERATORS[self.operator]

        n_ops = len(self.operands)
        assert n_ops == arity, \
               f"Wrong number of operands: expected {arity} but got {n_ops}"

        # TODO: refactor, get rid of type checking
        operands = [self.circuit[v].signal if isinstance(v, str) else v
                    for v in self.operands]

        if arity == 1:
            self._signal = getattr(operands[0], meth)()
        elif arity == 2:
            self._signal = getattr(operands[0], meth)(operands[1])

        self._signal += self._offset_16_bit()

        return self._signal

    def _offset_16_bit(self):
        """Operation NOT(int) is bitwise complement of int, that is, a number
        in which all 0s and 1s are swapped.
        In 16-bit space and with x=123, NOT(x) should be equal to
          65536 - x - 1 = 65412
        However, since python switched to INFINITE number of bits, __invert__()
        method produces just the 2nd term of the subtraction, such that
          NOT(x) = (123).__invert__() = -123 - 1 = -124
        To map it to 16-bit space, we have to further convert it by doing
          65536 - 124 = 65536 + (-124) = 65412
        """
        val = 0
        if self.operator == 'NOT':
            val = 65536
        return val

    def __repr__(self):
        return "<{} {}: {}({})>".format(
            self.__class__.__name__,
            self.name,
            self.operator,
            ",".join([str(v) for v in self.operands]))


CIRCUIT = Dict[str, Gate]


def create_circuit(lines: List[str]) -> CIRCUIT:
    circuit = {}
    for line in lines:
        line = line.strip()
        if line:
            gate = Gate.from_line(line)
            gate.connect_to(circuit)
    return circuit


def execute_circuit(circuit: CIRCUIT) -> None:
    for name, gate in circuit.items():
        gate.execute()
        if DEBUG:
            print(gate.name, gate.signal)


def reset_circuit(circuit: CIRCUIT) -> None:
    for name, gate in circuit.items():
        gate.reset()


def solve_p1(lines: List[str], target: str = None) -> int:
    """Solution to the 1st part of the challenge"""
    circuit = create_circuit(lines)
    if DEBUG:
        print(circuit)

    execute_circuit(circuit)

    if target is not None:
        return circuit[target].signal
    else:
        return {n: g.signal for n, g in circuit.items()}


def solve_p2(lines: List[str], target) -> int:
    """Solution to the 2nd part of the challenge"""
    circuit = create_circuit(lines)
    execute_circuit(circuit)

    signal_a = circuit['a'].signal
    reset_circuit(circuit)

    circuit['b'].signal = signal_a
    execute_circuit(circuit)

    return circuit[target].signal


text_1 = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""


tests = [
    (text_1.split('\n'),
     {'d': 72, 'e': 507, 'f': 492, 'g': 114, 'h': 65412, 'i': 65079,
      'x': 123, 'y': 456},
     None),
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
    day = '07'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 16076
    res1 = solve_p1(lines, 'a')
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 2797
    res2 = solve_p2(lines, 'a')
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
