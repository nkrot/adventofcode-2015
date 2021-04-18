#!/usr/bin/env python

# # #
# TODO
# 1) So many lines, fuck :(
# 2) How to formulate the problem in terms of Dijkstra shortest path algorithm?
# 3) The solution uses exceptions to control the flow of execution.
#    This should be changed to something less destructive.
# 4) see other TODOs scattered across the file

import re
import os
import sys
from typing import List, Tuple

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

    verbose = False

    items = {
        'M': 'MagicMissile',
        'D': 'Drain',
        'S': 'Shield',
        'P': 'Poison',
        'R': 'Recharge',
        #'D': 'Decay'
    }

    @classmethod
    def make_spells(cls, spec: str) -> List['Spell']:
        '''Given a specification <spec>, construct a list of spells that
        correspond to the specification. For example:
        >>> make_spells('MSD')
        >>> [MagicMissile(), Shield(), Drain()]
        '''
        spells = [getattr(sys.modules[__name__], cls.items[n])()
                  for n in spec.upper()]
        return spells

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

    def log(self, msg):
        if self.verbose:
            print(msg)


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
        self.log('Magic Missile deals {} damage.'.format(self.damage))
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
        self.log('Drain deals {} damage and heals {} hit points.'.format(
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
            self.log("Shield timer is now {}.".format(self.timer))
        else:
            self.log(
                "Shield increases armor by {}; its timer is now {}.".format(
                self.armor, self.timer))
            self.owner.armor += self.armor
            self.started = True
        if self.timer == 0:
            self.log("Shield wears off, decreasing armor by {}.".format(
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
        self.log('Poison deals {} damage; its timer is now {}.'.format(
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
        self.log("Recharge provides {} mana; its timer is now {}.".format(
                 self.mana, self.timer))
        self.owner.mana += self.mana


class Decay(Spell):
    '''
    Decay costs nothing
    It instantly does 1 damage and acts permanently.
    '''

    def __init__(self, target=None):
        super().__init__(0)
        self.damage = 1
        self.timer = 0
        self.target = target

    def act(self):
        self.log('Decay deals {} damage to {}.'.format(
                 self.damage, self.target.name))
        self.target.receives_attack(self.damage)

# GameOverError
# - BossLostError
# - WizardLostError
#   - WizardHasNoSpellsError
# - InvalidSpellError

class GameOverError(Exception):
    pass


class BossLostError(GameOverError):
    pass


class WizardLostError(GameOverError):
    pass


class WizardHasNoSpellsError(WizardLostError):
    pass


class InvalidSpellError(GameOverError):
    pass


class Player(object):

    @staticmethod
    def Wizard(spells=None):
        '''Standard Wizard player'''
        return Wizard(50, 500, spells)

    @staticmethod
    def Boss():
        '''Standard Boss player'''
        return Boss(51, 9)

    verbose = False

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

    def log(self, msg):
        if self.verbose:
            print(msg)


class Wizard(Player):
    '''Fights by casting spells'''

    def __init__(self, hp, mana=500, spells=None):
        super().__init__(hp)
        self.mana = mana
        self.mana_paid = 0
        self.mana_max_limit = None
        self.name = "Wizard"
        self._spells = []
        if spells:
            self.spells = spells

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
            #spell.target = self.opponent
            self._spells.append(spell)

    def act(self):
        if not self.spells:
            raise WizardHasNoSpellsError("No more spells available.")
        spell = self.spells.pop(0)
        self.buy_spell(spell)
        spell.target = self.opponent
        self.log(f"{self.name} casts {spell}.")
        self.scene.add_spell(spell)

    def die(self, reason='was killed'):
        self.log(f"Wizard dies: {reason}.")
        raise WizardLostError(f"Player {self.name} {reason}")

    def buy_spell(self, spell):
        '''If you cannot afford to cast any spell, you lose.'''
        if self.mana < spell.cost:
            self.die(f"not enough mana for {spell}")
        self.mana -= spell.cost
        self.mana_paid += spell.cost
        if self.mana_max_limit and self.mana_paid > self.mana_max_limit:
            self.die("Too much mana spent: {} > {}".format(
                self.mana_paid, self.mana_max_limit))


class Boss(Player):

    def __init__(self, hp, damage):
        super().__init__(hp)
        self.damage = damage
        self.name = "Boss"

    def __str__(self):
        return f"{self.name} has {self.hit_points} hit points"

    def act(self):
        self.log(f"Boss attacks for {self.damage} damage.")
        self.opponent.receives_attack(self.damage)

    def die(self):
        self.log("Boss dies.")
        raise BossLostError(f"Player {self.name} was killed.")


class Scene(object):
    '''Scene where all happens.'''

    def __init__(self):
        self.effects = []

    def add_spell(self, spell):
        '''Run given spell immediately or start an effect from it.'''
        if spell in self.effects:
            raise InvalidSpellError(
                f"Spell of type {type(spell)} is already active")
        if spell.timer == 0:
            # Spells with instant action
            spell.act()
        else:
            # Spells that create durable effects.
            # Effects become active in the next turn only.
            self.effects.append(spell)

    def act(self, turn=0):
        '''Run all effects available. Delete expired effects.
        This method should be triggered at the beginning of each turn.
        '''
        if self.effects:
            expired = []
            for idx, effect in enumerate(self.effects):
                effect.act()
                if not effect.is_active():
                    expired.append(idx)
            for idx in reversed(expired):
                self.effects.pop(idx)


class SceneWithDecay(Scene):
    '''
    A Scene that subtracts 1 hit point (causes 1 damage) to
    given target player before that players turn.
    '''
    def __init__(self, target: Tuple[int, Player]):
        '''Turns are numbered starting from 1'''
        super().__init__()
        self.turn_id, self.target = target  # Player affected by Decay effect

    def act(self, turn=0):
        '''If the turn=1, then it is Wizard (<self.target>) playing and he
        receives one Decay effect.
        '''
        if turn == self.turn_id:
            self.effects.insert(0, Decay(self.target))
        super().act()


class Battle(object):
    '''When a battle is over, this is indicated by throwing an exception'''

    verbose = False

    def __init__(self, scene, wizard, boss, descr=None):
        self.scene = scene
        self.players = [wizard, boss]
        self.description = descr or 'New Game'
        self.winner = None

        for i, j in [(0, 1), (1, 0)]:
            self.players[i].scene = self.scene
            self.players[i].opponent = self.players[j]

    def run(self):
        self.report(f"--- {self.description} ---")
        wizard, boss = self.players
        try:
            c_rounds = 0
            while True:
                c_rounds += 1

                self.report(f"\n-- Wizard turn, round {c_rounds} --")
                self.scene.act(1)
                wizard.act()

                self.report(f"\n-- Boss turn, round {c_rounds} --")
                self.scene.act(2)
                boss.act()

        except BossLostError:
            self.winner = (0, wizard)
            msg = f"Wizard won, mana spent: {wizard.mana_paid}."
            self.report(f"\n-- Game Over --\n{msg}")
            self.report()
            raise

        except WizardLostError:
            self.winner = (1, boss)
            msg = "Boss won. Try again."
            self.report(f"\n-- Game Over --\n{msg}")
            self.report()
            raise

    def report(self, msg=''):
        if self.verbose:
            print(msg)
            if msg:
                for pl in self.players:
                    print(f"- {pl}")


class BFSearchSolver(object):
    '''
    Algorithm
    The solver generates combinations of spells and runs the game (Battle)
    for each combination, memorizing games in which Wizard wins.

    Each game is always run from the very beginning.
    TODO: this could be improved by memoizing Battles for each combination
    of spells. When a new combination is spells is tried, the closest to it
    Battle can be retrieved from the memory and continued. For this, need to
    implement a copying mechanism for a Battle and its components (scene,
    players, spells).

    Combinations of spells are in generate a la BFS in a graph.
    If "a", "b" and "c" are individual spells, then the combinations are
    generated as follows:
    "a", "b", "c",
      "aa", "ab", "ac",
      "ba", "bb", "bc",
      "ca", "cb", "cc",
        "aaa", "aab", "aac",
        "aba", "abb", "abc",
        "aca", "acb", "acc",
        "baa", "bab", "bac",
        "bba", "bbb", "bbc",
        "bca", "bcb", "bcc",
        "cca", ...

    Optimizations
    -------------
    1) pruning: branches below the point where Wizard lost are not explored.
       Obviously, in those branches Wizard will loose as well.
    2) pruning: once a solution if found, the value of Mana spent is used to
       avoid exploring games (and games from their subbranches) as soon as such
       games show a higher value of Mana spent. If a new solution is better
       than the current one, the new one is used in further exploration.
    '''

    verbose = False

    def __init__(self):
        self.atoms = list(Spell.items.keys())
        self.combinations = list(self.atoms)

        # TODO: instead of functions that create objects, we can receive
        # and object and create copies of it when necessary
        self.create_boss_func = lambda: Player.Boss()
        self.create_wizard_func = lambda spells: Player.Wizard(spells)
        self.create_scene_func = lambda arg: Scene()  # ugly: arg not used

        # TODO:
        # Store found solution(s) and provide access to it/them
        # A solution is in this case the while Battle with players and spells

    def __iter__(self):
        return self

    def __next__(self):
        if self.combinations:
            curr = self.combinations.pop(0)
            self.combinations.extend([curr + atom for atom in self.atoms])
            return curr
        raise StopIteration

    def stop(self, comb: str):
        while self.combinations and self.combinations[-1].startswith(comb):
           deleted = self.combinations.pop()

    def run(self):

        solution = None
        cnt = 0

        for spec in self:
            cnt += 1

            boss = self.create_boss_func()
            wizard = self.create_wizard_func(Spell.make_spells(spec))
            if solution:
                wizard.mana_max_limit = solution[1].mana_paid

            # TODO: ugly:
            # in part 1, the argument will be ignored
            scene = self.create_scene_func((1, wizard))

            battle = Battle(scene, wizard, boss, f"New Game (#{cnt}): {spec}")

            try:
                battle.run()

            except WizardHasNoSpellsError:
                # Normal situation. keep searching
                self.log("No spells. Continue searching")
                pass

            except (InvalidSpellError, WizardLostError):
                # Stop exploring this branch of the graph
                self.stop(spec)

            except BossLostError:
                solution = (spec, wizard)
                self.log("Solution {} {}".format(solution, wizard.mana_paid))
                self.stop(spec)

        return solution[1].mana_paid if solution else -1

    def log(self, msg):
        if self.verbose:
            print(msg)


def set_verbosity(val):
    val = bool(val)
    Spell.verbose = val
    Player.verbose = val
    Battle.verbose = val
    BFSearchSolver.verbose = val


def demo_1():
    descr = "DEMO 1"
    spells = [Poison(), MagicMissile()]
    boss = Boss(13, 8)
    you = Wizard(10, 250, spells)
    battle = Battle(Scene(), you, boss, descr)
    try:
        battle.run()
    except GameOverError:
        pass


def demo_2():
    descr = "DEMO 2"
    spells = [Recharge(), Shield(), Drain(), Poison(), MagicMissile()]
    boss = Boss(14, 8)
    you = Wizard(10, 250, spells)
    battle = Battle(Scene(), you, boss, descr)
    try:
        battle.run()
    except GameOverError:
        pass


def demo_3_solve_p1():
    descr = "Solution to part 1"
    spells = [Poison(), Recharge(), MagicMissile(), Poison(), Shield(),
              MagicMissile(), MagicMissile(), MagicMissile()]
    boss = Player.Boss()
    you = Player.Wizard(spells)
    battle = Battle(Scene(), you, boss, descr)
    try:
        battle.run()
    except GameOverError:
        pass


def demo_4():
    descr = "DEMO 4 (with Decay effect on Wizard)"
    spells = [Recharge()]
    boss = Boss(14, 8)
    you = Wizard(1, 250, spells)
    scene = SceneWithDecay((1, you))
    battle = Battle(scene, you, boss, descr)
    try:
        battle.run()
    except GameOverError:
        pass


# for demos, set verbosity to True
#set_verbosity(True)
#demo_1()
#demo_2()
#demo_3_solve_p1()
#demo_4()
#exit(100)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    solver = BFSearchSolver()
    res = solver.run()
    return res


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    solver = BFSearchSolver()
    solver.create_scene_func = lambda arg: SceneWithDecay(arg)
    res = solver.run()
    return res


def run_real():
    day = '22'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 900
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 1216
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_real()
