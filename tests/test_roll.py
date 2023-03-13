from libse4x import roll_attack, roll_die
from libse4x import Upgrades
from libse4x.ships import *

def test_roll():
    assert 1 <= roll_die() <= 10

def test_attack():
    U = [[Upgrades(attack=a, defense=d) for d in range(4)] for a in range(4)]
    tests = [
        # test base numbers with simple upgrades
        [S_SCOUT , U[0][0], S_SCOUT, U[0][0], 0, 0, 3],
        [S_SCOUT , U[0][0], S_SCOUT, U[0][1], 0, 0, 2],
        [S_SCOUT , U[1][0], S_SCOUT, U[0][0], 0, 0, 4],
        [S_SCOUT , U[1][0], S_SCOUT, U[0][1], 0, 0, 3],
        [S_DESTRO, U[0][0], S_SCOUT, U[0][0], 0, 0, 4],
        [S_DESTRO, U[0][0], S_SCOUT, U[0][1], 0, 0, 3],
        [S_DESTRO, U[1][0], S_SCOUT, U[0][0], 0, 0, 5],
        [S_DESTRO, U[1][0], S_SCOUT, U[0][1], 0, 0, 4],
        # attacker's defense doesn't matter
        [S_SCOUT , U[0][1], S_SCOUT, U[0][0], 0, 0, 3],
        [S_SCOUT , U[0][1], S_SCOUT, U[0][1], 0, 0, 2],
        [S_SCOUT , U[1][1], S_SCOUT, U[0][0], 0, 0, 4],
        [S_SCOUT , U[1][1], S_SCOUT, U[0][1], 0, 0, 3],
        # defender's attack doesn't matter
        [S_SCOUT , U[0][0], S_SCOUT, U[1][0], 0, 0, 3],
        [S_SCOUT , U[0][0], S_SCOUT, U[1][1], 0, 0, 2],
        [S_SCOUT , U[0][1], S_SCOUT, U[1][0], 0, 0, 3],
        [S_SCOUT , U[0][1], S_SCOUT, U[1][1], 0, 0, 2],
        [S_SCOUT , U[1][0], S_SCOUT, U[1][0], 0, 0, 4],
        [S_SCOUT , U[1][0], S_SCOUT, U[1][1], 0, 0, 3],
        [S_SCOUT , U[1][1], S_SCOUT, U[1][0], 0, 0, 4],
        [S_SCOUT , U[1][1], S_SCOUT, U[1][1], 0, 0, 3],
        # attack limited by hull size
        [S_SCOUT , U[2][0], S_SCOUT, U[0][0], 0, 0, 4],
        # TODO: except for DDX where it's 2 instead of 1, both att and def
        # TODO: boarding tech attack and security tech
        # TODO: fighter tech attack and defense
        # TODO: raider tech attack
        # TODO: cloaked bonus on round 1 only
        # TODO: titan defense
        # TODO: titan fleet size bonus doesn't count
        # TODO: ...except for fighters
        # TODO: fighter attack bonus vs titans
        # TODO: fleet size bonus doesn't apply to boarding
        # TODO: fleet size bonus doesn't apply to ground combat
        # TODO: fleet size bonus doesn't apply to ground combat
        # TODO: hivemind bonuses
        # TODO: 1 roll is an autohit
        # TODO: 1 roll is not an autohit on titans
        # TODO: 2 roll is an autohit for DDX
        # TODO: 1 roll is an autohit for DDX on titans
        # TODO: attacker's ground combat units don't fire on first round, unless ground 3

    ]

    for i, line in enumerate(tests):
        _, _, tohit = roll_attack(line[0], line[2], line[1], line[3], line[4], line[5])
        assert tohit == line[6], f"[{i}] tohit expected: {line[6]} actual: {tohit}, {line}"
