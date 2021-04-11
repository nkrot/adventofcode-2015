#!/usr/bin/env python

# # #
# TODO
# 1) how to find combination of spells with minimal mana_paid value?
#    For the time being, the solution to p1 was found out manually :)
#    Alternatively:
#    Try finding the solution by doing BFS/DFS, where each vertex is
#    a spell. Prune (do not explore) branches that are worse than the best
#    solution found so far (that is, we need to find at least one solution
#    first).
# 2) So many lines, fuck :(
# 3) How to formulate the problem in terms of Dijkstra shortest path algorithm?

import re
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False

# Characteristics of a spell:
# 1) Instant or Effect
#    Instant is executed immediately and once.
#    Effect starts to work in the next turn and lasts for a number of turns.
# 2) Reversible or not.
#    Reversible is an effect that restores the state of the object once
#    the effect expired.
# 3) Onetime or Repeatable
#    Onetime -- affects the state of the object only once.
#    Repeatable -- on every turn, it affects the state of the object.


class Spell(object):

    def __init__(self, cost=0):
        self.cost = cost
        self.timer = 0      # has instant effect if time eq 0
        self.owner = None   # player who cast the spell
        self.target = None  # player against which the cast works

    def is_active(self):
        '''Tells if the spell is still active.

        NOTE: This makes sense for spells that cause an effect. This method
        should not be called for spells with instant action.
        '''
        return self.timer > 0

    def __str__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return isinstance(other, type(self))


class MagicMissile(Spell):
    '''
    Magic Missile costs 53 mana.
    It instantly does 4 damage.
    '''
    def __init__(self):
        super().__init__(53)
        self.damage = 4
        # self.damage = 13

    def __str__(self):
        return 'Magic Missile'

    def act(self):
        print('Magic Missile deals {} damage.'.format(self.damage))
        self.target.receives_attack(self.damage)


class Drain(Spell):
    '''
    Drain costs 73 mana.
    It instantly does 2 damage and heals you for 2 hit points.
    '''
    def __init__(self):
        super().__init__(73)
        self.damage = 2
        self.hit_points = 2

    def act(self):
        print('Drain deals {} damage and heals {} hit points.'.format(
            self.damage, self.hit_points))
        self.owner.hit_points += self.hit_points
        self.target.receives_attack(self.damage)


class Shield(Spell):
    '''
    Shield costs 113 mana.
    It starts an effect that lasts for 6 turns.
    While it is active, your armor is increased by 7.
    '''

    def __init__(self):
        super().__init__(113)
        self.timer = 6
        self.armor = 7
        self.started = False

    def act(self):
        assert self.is_active(), "Ops. should not be called."
        self.timer -= 1
        if self.started:
            print("Shield timer is now {}.".format(self.timer))
        else:
            print("Shield increases armor by {}; its timer is now {}.".format(
                self.armor, self.timer))
            self.owner.armor += self.armor
            self.started = True
        if self.timer == 0:
            print("Shield wears off, decreasing armor by {}.".format(
                self.armor))
            self.owner.armor -= self.armor


class Poison(Spell):
    '''
    Poison costs 173 mana.
    It starts an effect that lasts for 6 turns.
    At the start of each turn while it is active, it deals the boss 3 damage.
    '''

    def __init__(self):
        super().__init__(173)
        self.timer = 6
        self.damage = 3

    def __str__(self):
        return 'Poison'

    def act(self):
        assert self.is_active(), "Ops. should not be called."
        self.timer -= 1
        print('Poison deals {} damage; its timer is now {}.'.format(
            self.damage, self.timer))
        self.target.receives_attack(self.damage)


class Recharge(Spell):
    '''
    Recharge costs 229 mana.
    It starts an effect that lasts for 5 turns.
    At the start of each turn while it is active, it gives you 101 new mana.
    '''
    def __init__(self):
        super().__init__(229)
        self.timer = 5
        self.mana = 101

    def act(self):
        assert self.is_active(), "Ops. should not be called."
        self.timer -= 1
        print("Recharge provides {} mana; its timer is now {}.".format(
            self.mana, self.timer))
        self.owner.mana += self.mana


class Decay(Spell):
    '''
    Decay costs nothing
    It instantly does 1 damage and acts permamently.
    '''

    def __init__(self, target=None):
        super().__init__(0)
        self.damage = 1
        self.timer = 0
        self.target = target

    def act(self):
        print('Decay deals {} damage to {}.'.format(
            self.damage, self.target.name))
        self.target.receives_attack(self.damage)


class BossLost(Exception):
    pass


class WizardLost(Exception):
    pass


class Player(object):

    @staticmethod
    def Wizard():
        '''Standard Wizard player'''
        return Wizard(50, 500)

    @staticmethod
    def Boss():
        '''Standard Boss player'''
        return Boss(51, 9)

    def __init__(self, hp):
        self.hit_points = hp  # health
        self.armor = 0
        self.opponent = None  # the other player
        self.name = "NONAME"
        self.scene = None

    def receives_attack(self, damage):
        self.hit_points -= max(1, damage - self.armor)
        if self.hit_points < 1:
            self.die()


class Wizard(Player):
    '''Fights by casting spells'''

    def __init__(self, hp, mana=500):
        super().__init__(hp)
        self.mana = mana
        self.mana_paid = 0
        self.name = "Wizard"
        self._spells = []

    def __str__(self):
        return "{} has {} hit points, {} armor, {} mana; spent {} mana".format(
            self.name, self.hit_points, self.armor, self.mana, self.mana_paid)

    @property
    def spells(self):
        return self._spells

    @spells.setter
    def spells(self, _spells):
        for spell in _spells:
            spell.owner = self
            spell.target = self.opponent
            self._spells.append(spell)

    def act(self):
        if not self.spells:
            self.die("no spells available")
        spell = self.spells.pop(0)
        self.buy_spell(spell)
        print(f"{self.name} casts {spell}.")
        self.scene.add_spell(spell)

    def die(self, reason='was killed'):
        print(f"Wizard dies: {reason}.")
        raise WizardLost(f"Player {self.name} {reason}")

    def buy_spell(self, spell):
        '''If you cannot afford to cast any spell, you lose.'''
        if self.mana < spell.cost:
            self.die(f"not enough mana for {spell}")
        self.mana -= spell.cost
        self.mana_paid += spell.cost


class Boss(Player):

    def __init__(self, hp, damage):
        super().__init__(hp)
        self.damage = damage
        self.name = "Boss"

    def __str__(self):
        return f"{self.name} has {self.hit_points} hit points"

    def act(self):
        print(f"Boss attacks for {self.damage} damage.")
        self.opponent.receives_attack(self.damage)

    def die(self):
        print("Boss dies.")
        raise BossLost(f"Player {self.name} was killed.")


class Scene(object):
    '''Scene where all happens.'''

    def __init__(self):
        self.effects = []

    def add_spell(self, spell):
        '''Run given spell immediately or start an effect from it.'''
        # + [DONE] test that this may kill the opponent immediately
        if spell in self.effects:
            raise ValueError(f"Spell of type {type(spell)} is already active")
        if spell.timer == 0:
            # Spells with instant action
            spell.act()
        else:
            # Spells that create effects.
            # Effects become active in the next turn.
            self.effects.append(spell)

    def act(self):
        '''Run all effects available. Delete expired effects.
        This method should be triggered at the beginning of each turn.
        '''
        if self.effects:
            expired = []
            for idx, effect in enumerate(self.effects):
                effect.act()
                if not effect.is_active():
                    expired.append(idx)
            if expired:
                for idx in reversed(expired):
                    self.effects.pop(idx)


class SceneWithDecay(Scene):
    '''
    A Scene that subtracts 1 hit point (causes 1 damage) before every turn
    '''
    def __init__(self, target):
        super().__init__()
        self.target = target  # Player affected by Decay effect

    def act(self):
        self.effects.insert(0, Decay(self.target))
        super().act()


def report(msg, players):
    print(msg)
    for pl in players:
        print(f"- {pl}")


def play(scene, you, boss, spells, msg=None):
    msg = msg or 'New Game'
    print(f"--- {msg} ---")

    you.opponent = boss
    boss.opponent = you

    you.scene = scene
    you.spells = spells

    try:
        c_rounds = 0
        while True:
            c_rounds += 1

            report(f"\n-- Wizard turn, round {c_rounds} --", [you, boss])
            scene.act()
            you.act()

            report(f"\n-- Boss turn, round {c_rounds} --", [you, boss])
            scene.act()
            boss.act()

    except BossLost:
        msg = f"Wizard won, mana spent: {you.mana_paid}."
        winner = (0, you)

    except WizardLost:
        msg = "Boss won. Try again."
        winner = (1, boss)

    report(f"\n-- Game Over --\n{msg}", [you, boss])
    print()

    return winner


def demo_1():
    descr = "DEMO 1"
    boss = Boss(13, 8)
    you = Wizard(10, 250)
    spells = [Poison(), MagicMissile()]
    play(Scene(), you, boss, spells, descr)


def demo_2():
    descr = "DEMO 2"
    boss = Boss(14, 8)
    you = Wizard(10, 250)
    spells = [Recharge(), Shield(), Drain(), Poison(), MagicMissile()]
    play(Scene(), you, boss, spells, descr)


def demo_3():
    descr = "DEMO 3 (with Decay effect)"
    boss = Boss(14, 8)
    you = Wizard(1, 250)
    spells = [Recharge()]
    play(SceneWithDecay(you), you, boss, spells, descr)

#demo_1()
#demo_2()
#demo_3()
#exit(100)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""

    you = Player.Wizard()
    boss = Player.Boss()

    # mana spent: 1242 (too high)
    spells = [Shield(), Recharge(), Poison(),
              MagicMissile(), MagicMissile(), Shield(), Recharge(), Poison(),
              MagicMissile(), MagicMissile()]

    # mana spent: 1256
    spells = [Poison(), Recharge(), Shield(), Poison(),
              MagicMissile(), Recharge(), Poison(), Shield()]

    # mana spent: 900
    spells = [Poison(), Recharge(), MagicMissile(), Poison(), Shield(),
              MagicMissile(), MagicMissile(), MagicMissile()]

    winner = play(Scene(), you, boss, spells)

    if winner[0] == 0:
        return winner[1].mana_paid

    return -1


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""

    you = Player.Wizard()
    boss = Player.Boss()

    # mana spent: 1784 (too high)
    spells = [Shield(), Drain(), Recharge(),
              Shield(), Poison(), Recharge(),
              Shield(), Poison(), Recharge(),
              Shield(), Poison(), MagicMissile()
              ]

    # mana spent: 1940
    spells = [Shield(), MagicMissile(), Recharge(),
              Shield(), Poison(), Recharge(),
              Shield(), Poison(), Recharge(),
              Shield(), Poison(), Recharge() ]

    # mana spent: 1422 (too high)
    spells = [Shield(), Recharge(), Poison(),
              Shield(), Recharge(), Poison(),
              Shield(), MagicMissile(), Poison(),
              MagicMissile()]

    # mana spent: 1355 (too high)
    spells = [Shield(), Recharge(), Poison(),
              Shield(), Recharge(), Poison(),
              Shield(), MagicMissile(), MagicMissile(),
              MagicMissile(), MagicMissile()
              ]

    # mana spent: 1256
    spells = [Poison(), Recharge(), Shield(),
              Poison(), Recharge(), Shield(),
              Poison(), MagicMissile()]

    # # mana spent:
    # spells = [Poison(), Recharge(), Shield(),
    #           Poison(), Recharge(), Shield(),
    #           Poison(), MagicMissile(), MagicMissile()
    #           ]

    # TODO: not working yet

    winner = play(SceneWithDecay(you), you, boss, spells)

    if winner[0] == 0:
        return winner[1].mana_paid

    return -1


def run_real():
    day = '22'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 900
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    # print(f"--- Day {day} p.2 ---")
    # exp2 = -1
    # res2 = solve_p2(lines)
    # print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_real()
