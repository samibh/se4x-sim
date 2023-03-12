#!/usr/bin/python3

"""
libse4x 0.1
A fight simulator for the boardgame Space Empires: 4X and Space Empires: Close Encounters

This is still a very rough initial version. Hopefully it gives accurate results, but
there may be hidden bugs, edge cases or mistakes lurking.

Example usage (a jupyter notebook sample is included):

    from libse4x import Upgrades, fight

    att_fleet = [S_DREAD]*2
    def_fleet = [S_FIGHTER,S_FIGHTER,S_FIGHTER,S_FIGHTER,S_FIGHTER,S_FIGHTER,S_CARRIER,S_CARRIER]

    # Simulate a single fight with verbose output
    nb_att, nb_def, next_ships, att_cp_lost, def_cp_lost = fight(
                att_fleet, Upgrades(attack=3,defense=3),
                def_fleet, Upgrades(attack=1,defense=1,fighter=3),
                verbose=True)
    print("Att CP lost: {} - Def CP lost : {}".format(att_cp_lost, def_cp_lost))

    # Sample output with 1 scout 0-0 (attacker) vs 1 scout 1-1 (defender) :
    # Combat starting. 1 ATT vs. 1 DEF
    # DEF Scout         at 1/1 hp, prio : 5.80
    # ATT Scout         at 1/1 hp, prio : 5.90
    # --------------------------------------------------------------------------------
    #     DEF Scout         [0] rolls  7/ 4 vs. ATT Scout         [1]
    #     ATT Scout         [1] rolls  5/ 2 vs. DEF Scout         [0]
    # Combat round 1 finished. Ships left : 1 ATT vs. 1 DEF
    # --------------------------------------------------------------------------------
    #     DEF Scout         [0] rolls  4/ 4 vs. ATT Scout         [1]
    # ATT Scout [1] hit by Scout [0] (roll:4/4)
    # ATT Scout [1] destroyed by Scout [0] (roll:4/4)
    # DEF Scout         at 1/1 hp, prio : 5.80 X
    # ATT Scout         at 0/1 hp, prio : 5.90 DEAD
    # Combat round 2 finished. Ships left : 0 ATT vs. 1 DEF
    # --------------------------------------------------------------------------------
    # Combat finished. Ships left : 0 ATT vs. 1 DEF
    # DEF Scout         at 1/1 hp, prio : 5.80 X
    # ATT Scout         at 0/1 hp, prio : 5.90 DEAD
    # ================================================================================
    # Att CP lost: 6 - Def CP lost : 0

    # Simulate a fight multiple times, output the average winrate and lost CP for each side
    nb_sims = 2000
    att_wins = 0
    def_wins = 0
    att_cps_lost = 0
    def_cps_lost = 0

    for i in range(nb_sims):
        nb_att, nb_def, next_ships, att_cp_lost, def_cp_lost = fight(
                    att_fleet, Upgrades(attack=3,defense=3),
                    def_fleet, Upgrades(attack=1,defense=1,fighter=3))
        att_cps_lost += att_cp_lost
        def_cps_lost += def_cp_lost
        if nb_att == 0:
            def_wins += 1
        else:
            att_wins += 1

    print('{:5} sims, ATT won {:2.0f}% [lost:{:.1f}], DEF won {:2.0f}% [lost:{:.1f}]'.format(
        nb_sims, 100. * att_wins / nb_sims, 1. * att_cps_lost / nb_sims,
                 100. * def_wins / nb_sims, 1. * def_cps_lost / nb_sims))

    # Sample output:
    # 2000 sims, ATT won 53% [lost:29.5], DEF won 47% [lost:29.3]

License:
    Copyright (c) 2018, Sami Ben Hatit

    All rights reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    Except as contained in this notice, the name of a copyright holder shall not
    be used in advertising or otherwise to promote the sale, use or other dealings
    in this Software without prior written authorization of the copyright holder.

Credits:
    Space Empires: 4X is an excellent game by:
    DESIGNER: Jim Krohn
    DEVELOPER: Martin Scott
    ART DIRECTOR/PACKAGE ART: Rodger B. MacGowan
    MAP & COUNTER ART: Mark Simonitch
    PRODUCERS: Andy Lewis, Gene Billingsley, Mark Simonitch, Rodger MacGowan, & Tony Curtis

    Space Empires: Close Encounters is the also excellent first expansion by:
    DESIGNER: Jim Krohn
    DEVELOPER: Oliver Upshaw
    COVER ART: Eric Williams
    ART DIRECTOR, PACKAGING: Rodger B. MacGowan
    COUNTER ART: Mark Simonitch
    PRODUCERS: Andy Lewis, Gene Billingsley, Mark Simonitch, Rodger MacGowan, & Tony Curtis
"""

import random
from collections import defaultdict, namedtuple
from copy import deepcopy
from operator import itemgetter

#pylint: disable-msg=too-many-arguments

"""
=============================================================================
Ship types
- name   user-friendly name
- cost   CP cost
- prio   Attack priority A:1 B:2 C:3 D:4 E:5 F:6
- att    Base attack
- def    Base defense
- size   Hull size
=============================================================================
"""
# Ship = namedtuple('Ship', ['name', 'cost', 'prio', 'att', 'def', 'size'])

S_SCOUT        = {'name':'Scout'        , 'cost': 6, 'prio':5, 'att':3, 'def':0, 'size':1}
S_DESTRO       = {'name':'Destroyer'    , 'cost': 9, 'prio':4, 'att':4, 'def':0, 'size':1}
S_CRUISER      = {'name':'Cruiser'      , 'cost':12, 'prio':3, 'att':4, 'def':1, 'size':2}
S_BC           = {'name':'Battlecruiser', 'cost':15, 'prio':2, 'att':5, 'def':1, 'size':2}
S_BB           = {'name':'Battleship'   , 'cost':20, 'prio':1, 'att':5, 'def':2, 'size':3}
S_DREAD        = {'name':'Dreadnaught'  , 'cost':24, 'prio':1, 'att':6, 'def':3, 'size':3}
S_TITAN        = {'name':'Titan'        , 'cost':32, 'prio':1, 'att':7, 'def':3, 'size':5}

S_BOARD        = {'name':'Boarding'     , 'cost':12, 'prio':6, 'att':5, 'def':0, 'size':2}
S_CARRIER      = {'name':'Carrier'      , 'cost': 5, 'prio':5, 'att':3, 'def':1, 'size':1}
S_FIGHTER      = {'name':'Fighter'      , 'cost': 5, 'prio':2, 'att':5, 'def':0, 'size':1}

S_TRANSPORT    = {'name':'Transport'    , 'cost': 6, 'prio':5, 'att':1, 'def':1, 'size':1}
S_MILITIA      = {'name':'Militia'      , 'cost': 0, 'prio':5, 'att':5, 'def':0, 'size':1, 'ground': True}
S_INFANTRY     = {'name':'Infantry'     , 'cost': 2, 'prio':4, 'att':5, 'def':1, 'size':1, 'ground': True}
S_MARINE_ATT   = {'name':'Marines (att)', 'cost': 3, 'prio':3, 'att':6, 'def':1, 'size':2, 'ground': True}
S_MARINE_DEF   = {'name':'Marines (def)', 'cost': 3, 'prio':4, 'att':5, 'def':1, 'size':2, 'ground': True}
S_HI_ATT       = {'name':'Hvy inf (att)', 'cost': 3, 'prio':4, 'att':4, 'def':2, 'size':2, 'ground': True}
S_HI_DEF       = {'name':'Hvy inf (def)', 'cost': 3, 'prio':3, 'att':6, 'def':2, 'size':2, 'ground': True}
S_GRAV         = {'name':'Grav Armor'   , 'cost': 4, 'prio':3, 'att':6, 'def':2, 'size':2, 'ground': True}

S_BASE         = {'name':'Base'         , 'cost':12, 'prio':1, 'att':7, 'def':2, 'size':3}
S_SHIPYARD     = {'name':'Shipyard'     , 'cost': 6, 'prio':3, 'att':3, 'def':1, 'size':1}

S_RAIDER_NOCLK = {'name':'Raider'       , 'cost':12, 'prio':4, 'att':4, 'def':0, 'size':2}
S_RAIDER_CLK   = {'name':'Raider (clkd)', 'cost':12, 'prio':1, 'att':5, 'def':0, 'size':2}

S_SWEEPER      = {'name':'Sweeper'      , 'cost': 6, 'prio':5, 'att':1, 'def':0, 'size':1}

S_DDX          = {'name':'DDX'          , 'cost': 9, 'prio':4, 'att':4, 'def':0, 'size':1}

S_ALIENB       = {'name':'Alien B'      , 'cost': 0, 'prio':2, 'att':6, 'def':2, 'size':1}
S_ALIENC       = {'name':'Alien C'      , 'cost': 0, 'prio':3, 'att':5, 'def':2, 'size':1}
S_ALIEND       = {'name':'Alien D'      , 'cost': 0, 'prio':4, 'att':4, 'def':1, 'size':1}

S_FLAGSHIP     = {'name':'HMS Jeff'     , 'cost': 0, 'prio':2, 'att':4, 'def':1, 'size':3}

#Insectoids
S_BOARD_INS    = {'name':'Boarding (insectoids)', 'cost':12, 'prio':6, 'att':5, 'def':0, 'size':1}

# Cloaking geniuses
S_SCOUT_CG     = {'name':'Scout clkd'    , 'cost': 6, 'prio':1, 'att':3, 'def':0, 'size':1}
S_DESTRO_CG    = {'name':'Destroyer clkd', 'cost': 9, 'prio':1, 'att':4, 'def':0, 'size':1}
S_CRUISER_CG   = {'name':'Cruiser clkd'  , 'cost':12, 'prio':1, 'att':4, 'def':1, 'size':2}

# =============================================================================
class Upgrades:
    """Describes upgrades applicable to a ship"""
    # pylint: disable=too-many-instance-attributes, too-few-public-methods
    def __init__(self, attack=0, defense=0, boarding=0, security=0, cloaking=0, fighter=0,
                 tactics=0, transport=0, immortal=False, giant=False, hivemind=False):
        # Combat tech
        self.attack = attack
        self.defense = defense
        self.boarding = boarding
        self.security = security
        self.cloaking = cloaking
        self.fighter = fighter
        self.tactics = tactics
        self.transport = transport
        # Race bonus
        self.immortal = immortal
        self.giant = giant
        self.hivemind = hivemind

    def __copy__(self):
        copy = self.__class__
        result = copy.__new__(copy)
        result.__dict__.update(self.__dict__)
        return result

# =============================================================================
# Private methods
# =============================================================================

ATTACKER = 'ATT'
DEFENDER = 'DEF'

def roll_die():
    """Simulate a single roll of a 10-sided die"""
    roll = random.randint(1, 10)
    return roll

def roll_attack(att_ship, def_ship, att_upgrades, def_upgrades, bonus_fleet=0, nb_round=0):
    """
    Simulates a roll between attacker ship with attacker upgrades
                         vs. defender ship with defender upgrades
    Returns :
        1+   attacker has 1+ hit or boarded defender
        0    attacker has 0 hit (missed)

    DONE : raider +1 bonus on first round of combat
    TODO : transport upgrades
    """

    att_name = att_ship['name']
    def_name = def_ship['name']

    # Att/def upgrades are capped by hull size, except for DDX
    if 'DDX' in att_name:
        att_up = min(att_upgrades.attack, att_ship['size']+1)
    else:
        att_up = min(att_upgrades.attack, att_ship['size'])

    if 'DDX' in def_name:
        def_up = min(def_upgrades.defense, def_ship['size']+1)
    else:
        def_up = min(def_upgrades.defense, def_ship['size'])

    # Fighter 3 upgrade gives +1 def
    if 'Fighter' in def_name and def_upgrades.fighter >= 3:
        def_up += 1

    # Base formula (no specials) :
    # roll = attacker_att + attacker_upgrade - defender_defense - defender_upgrade
    tohit = att_ship['att'] + att_up - def_ship['def'] - def_up

    # - boarding ATT : attack score = 4 + boarding_tech - defender_size - defender_security
    if 'Boarding' in att_name:
        tohit = att_ship['att'] + att_upgrades.boarding - 1 - def_ship['size'] - def_upgrades.security

    # - fighter ATT = 4 + fighter_tech + attack_upgrade - defender_defense - defender_upgrade
    elif 'Fighter' in att_name:
        tohit += att_upgrades.fighter - 1

    # - raider ATT : attack score = 3 + raider_tech + attack_upgrade - defender_defense - defender_upgrade
    #                               (+1 if first round of combat)
    elif 'Raider' in att_name:
        tohit += att_upgrades.cloaking - 1


    if 'Titan' in def_ship['name']:
        # - titan DEF : titans cannot be boarded
        if 'Boarding' in att_name:
            result = 0
            return result
        # - titan DEF : fighters get +1 att vs titan
        elif 'Fighter' in att_name:
            tohit += 1

    roll = roll_die()

    # fleet size bonus, doesn't apply to boarding, and only benefits Fighters vs Titans
    if not 'Boarding' in att_name and ('Fighter' in att_name or (not 'Titan' in def_ship['name'])) and not att_ship.get('ground'):
        tohit += bonus_fleet

    # cloaked ships have +1 attack in first round of combat
    if nb_round == 1 and 'clkd' in att_name:
        tohit += 1

    # Attacker's ground combat units don't fire on first round unless they have ground 3
    if nb_round == 1 and att_ship.get('ground') and att_upgrades.transport < 3 and att_ship['side'] == ATTACKER:
        return 0, 10, 0

    if att_upgrades.hivemind and nb_round >= 4:
        tohit += 1
    if def_upgrades.hivemind and nb_round >= 2:
        tohit -= 1

    # a 1 roll is an auto hit
    # - titan DEF : 1 does not auto-hit
    if not 'Titan' in def_ship['name']:
        tohit = max(tohit, 1)

    if roll <= tohit:
        result = 1
    else:
        result = 0


    # - titan ATT : 2 damage
    if 'Titan' in att_name:
        result *= 2

    return result, roll, tohit

def find_defender(ships, side):
    """
    Crude method to find something approximating the best target when attacking
    ships is a list of extended ship dictionaries
        {
            'name': 'Militia', 'cost': 0, 'prio': 5, 'att': 5, 'def': 0, 'size': 1,
            'ground': True, 'order': 5.8, 'hp': 1, 'upgrades': Upgrades(...), 'hasfired': False, 'skipuntil': 0,
            'side': 'DEF'
        }
    TODO: more useful shape, hard to tell which ship has the highest attack for example, as upgrades aren't applied
          (not trivial for all cases though, as it may depend on ship<->ship interactions, eg point defense
    """
    enemies = [x for x in ships if x['side'] != side and x['hp'] > 0]
    if not enemies:
        return None

    # shoot already wounded enemies first
    wounded = [x for x in enemies if x['hp'] < x['size']]
    if wounded:
        found = ships.index(wounded[0])
        return found

    # shoot boarders in priority (?)
    boarding = [x for x in enemies if 'Boarding' in x['name']]
    if boarding:
        found = ships.index(boarding[0])
        return found

    # shoot 1 hp ships
    hp_1 = [x for x in enemies if x['size'] == 1]
    if hp_1:
        found = ships.index(hp_1[0])
        return found

    # shoot 2 hp ships
    hp_2 = [x for x in enemies if x['size'] == 2]
    if hp_2:
        found = ships.index(hp_2[0])
        return found

    # otherwise just shoot the first one (??!)
    found = ships.index(enemies[0])
    return found

def minidump_ships(ships):
    """Debug logging: dump all the ships in the fight and their state"""
    for ship in ships:
        if ship['hp'] <= 0:
            comment = 'DEAD'
        elif ship['skipuntil']:
            comment = 'SKIP'
        elif ship['hasfired']:
            comment = 'X'
        else:
            comment = ''
        print('{} {:13} at {}/{} hp, prio : {:.2f} {}'
              .format(ship['side'], ship['name'], ship['hp'], ship['size'], ship['order'], comment))

def show_roll(roll, tohit, iatt, attacker, idef, defender):
    """Debug logging: display a die roll and context"""
    print('    {} {:13} [{}] rolls {:2}/{:2} vs. {} {:13} [{}]'
          .format(attacker['side'], attacker['name'], iatt, roll, tohit, defender['side'], defender['name'], idef))

# =============================================================================
# Public methods
# =============================================================================

def fight(att_fleet, att_upgrades, def_fleet, def_upgrades, verbose=False, asteroids=False, nebula=False):
    """
    Simulate a full fight between att_fleet and def_fleet.
    Input :
        att_fleet       list of ships in the attacking fleet
                        e.g. [S_BOARD,S_BOARD,S_BOARD]
        def_fleet       list of ships in the defending fleet
                        e.g. [S_CRUISER,S_CRUISER]
        xyz_upgrades    upgrades for all ships in the xyz fleet
        verbose         if True, output debugging log with detailed rolls and ships state

    ships : list of ships extended with following properties :
                order      firing order (lower fires first)
                hp         hp left (max size)
                upgrades   upgrades of this ship
                hasfired   flag if still has to fire each round
                skipuntil  if > 0, the ship is inactive until the round number 'skipuntil'
                side       1 = attacker
                           0 = defender

    DONE : fleet size bonus at beginning of each round
    DONE : captured ships can't fire for one round
    TODO : racials (in progress)
    TODO : better priority targeting
    TODO : different upgrades for each ship in a fleet
    TODO : asteroids/nebula probably buggy for boarding
    """

    if att_upgrades.immortal:
        immortal = ATTACKER
    elif def_upgrades.immortal:
        immortal = DEFENDER
    else:
        immortal = None

    if asteroids:
        att_upgrades.attack = 0
        def_upgrades.attack = 0
    if nebula:
        att_upgrades.defense = 0
        def_upgrades.defense = 0

    # CP lost on either side
    att_cp_lost = 0
    def_cp_lost = 0

    att_ships = []
    def_ships = []
    for x in att_fleet:
        ship = dict(x)
        if asteroids or nebula:
            ship['order'] = .9 - att_upgrades.tactics / 5
        else:
            ship['order'] = ship['prio'] + .9 - att_upgrades.tactics / 5
        ship['hp'] = ship['size']
        ship['upgrades'] = att_upgrades
        ship['hasfired'] = False
        ship['skipuntil'] = 0
        ship['side'] = ATTACKER
        if att_upgrades.giant:
            ship['size'] += 1
        att_ships.append(ship)
    for x in def_fleet:
        ship = dict(x)
        if asteroids or nebula:
            ship['order'] = .8 - def_upgrades.tactics / 5
        else:
            ship['order'] = ship['prio'] + .8 - def_upgrades.tactics / 5
        ship['hp'] = ship['size']
        ship['upgrades'] = def_upgrades
        ship['hasfired'] = False
        ship['skipuntil'] = 0
        ship['side'] = DEFENDER
        if def_upgrades.giant:
            ship['size'] += 1
        def_ships.append(ship)

    ships = att_ships
    ships.extend(def_ships)
    ships_sorted = sorted(ships, key=itemgetter('order'))

    nb_att = len(att_fleet)
    nb_def = len(def_fleet)
    capture = False # no capture last round
    nb_round = 1

    if verbose:
        print('Combat starting. {} ATT vs. {} DEF'.format(nb_att, nb_def))
        minidump_ships(ships_sorted)
        print('-'*80)

    while nb_att > 0 and nb_def > 0:
        # Main fight loop : new combat round

        # Make sure ships are still sorted by order (if a ship is captured and switches side)
        if capture:
            ships_sorted = sorted(ships_sorted, key=itemgetter('order'))
            capture = False

        # If there are fighters AND point defense scouts, have them fire in A
        # TODO

        # Reset all "has_fired" flags
        for x in ships_sorted:
            x['hasfired'] = False

        # Check for fleet size bonus
        if nb_att >= 2 * nb_def:
            fleet_bonus = ATTACKER
        elif nb_def >= 2 * nb_att:
            fleet_bonus = DEFENDER
        else:
            fleet_bonus = None

        # Reset immortal use
        immortal_used = False

        # By firing order, each ship tht has not fired yet at an enemy
        next_ships = deepcopy(ships_sorted)

        for i_att, _ in enumerate(ships_sorted):

            att_ship = next_ships[i_att]

            i_def = find_defender(next_ships, att_ship['side'])
            if i_def is None:
                if verbose:
                    print('No more defenders found vs. {} {}. Fight finished!'.format(att_ship['side'], att_ship['name']))
                break
            def_ship = next_ships[i_def]

            # dead ships
            if att_ship['hp'] <= 0:
                continue
            # captured ships can't fire for one round
            if att_ship['skipuntil'] > nb_round:
                continue
            # should not happen...
            if att_ship['hasfired']:
                print('WARNING! this ship has already fired ?!')
                print(att_ship)
                continue

            bonus = 1 if att_ship['side'] == fleet_bonus else 0
            hits, roll, tohit = roll_attack(att_ship, def_ship, att_ship['upgrades'], def_ship['upgrades'], bonus, nb_round)
            if verbose:
                show_roll(roll, tohit, i_att, att_ship, i_def, def_ship)

            att_ship['hasfired'] = True

            # Special case of boarding
            if 'Boarding' in att_ship['name']:
                if hits > 0:
                    # vessel captured
                    if verbose:
                        print("{} {} [{}] captured by {} [{}] (roll:{}/{})".format(def_ship['side'], def_ship['name'], i_def, att_ship['name'], i_att, roll, tohit))
                    capture = True
                    if def_ship['side'] == DEFENDER:
                        nb_def -= 1
                        nb_att += 1
                        def_ship['side'] = ATTACKER
                        def_ship['hasfired'] = True # ?
                        prio_malus = .1
                        def_cp_lost += def_ship['cost']
                        att_cp_lost -= def_ship['cost']
                    else:
                        nb_def += 1
                        nb_att -= 1
                        def_ship['side'] = DEFENDER
                        def_ship['hasfired'] = True # ?
                        prio_malus = 0
                        def_cp_lost -= def_ship['cost']
                        att_cp_lost += def_ship['cost']
                    def_ship['order'] = def_ship['prio'] + .8 + prio_malus - def_ship['upgrades'].tactics / 5
                    # captured ships can't fire for one round
                    def_ship['skipuntil'] = nb_round + 2
                    if verbose:
                        minidump_ships(next_ships)
            # General case
            else:
                if hits > 0:
                    if immortal == def_ship['side'] and not immortal_used:
                        immortal_used = True
                        hits -= 1
                        if verbose:
                            print("** Immortal used **")
                    if hits > 0:
                        def_ship['hp'] -= hits
                        if verbose:
                            print("{} {} [{}] hit by {} [{}] (roll:{}/{})".format(def_ship['side'], def_ship['name'], i_def, att_ship['name'], i_att, roll, tohit))
                        # Check if defender has been destroyed
                        if def_ship['hp'] <= 0:
                            # vessel destroyed
                            if verbose:
                                print("{} {} [{}] destroyed by {} [{}] (roll:{}/{})".format(def_ship['side'], def_ship['name'], i_def, att_ship['name'], i_att, roll, tohit))
                            if def_ship['side'] == DEFENDER:
                                nb_def -= 1
                                def_cp_lost += def_ship['cost']
                            else:
                                nb_att -= 1
                                att_cp_lost += def_ship['cost']
                        if verbose:
                            minidump_ships(next_ships)

        ships_sorted = next_ships
        if verbose:
            print('Combat round {} finished. Ships left : {} ATT vs. {} DEF'.format(nb_round, nb_att, nb_def))
            print('-'*80)
        nb_round += 1

    if verbose:
        print('Combat finished. Ships left : {} ATT vs. {} DEF'.format(nb_att, nb_def))
        minidump_ships(next_ships)
        print('='*80)

    return (nb_att, nb_def, next_ships, att_cp_lost, def_cp_lost)


def multifight(att_fleet, att_upgrades, def_fleet, def_upgrades, nb_sims=2000, asteroids=False, nebula=False):
    att_wins = 0
    def_wins = 0
    att_cps_lost = 0
    def_cps_lost = 0
    for i in range(nb_sims):
        nb_att, nb_def, next_ships, att_cp_lost, def_cp_lost = fight(
            att_fleet, att_upgrades,
            def_fleet, def_upgrades,
            asteroids=asteroids, nebula=nebula,
        )
        att_cps_lost += att_cp_lost
        def_cps_lost += def_cp_lost
        if nb_att == 0:
            def_wins += 1
        else:
            att_wins += 1

    print('{:5} sims, ATT won {:2.0f}% [lost:{:.1f}], DEF won {:2.0f}% [lost:{:.1f}]'.format(
        nb_sims,
        100. * att_wins / nb_sims, 1. * att_cps_lost / nb_sims,
        100. * def_wins / nb_sims, 1. * def_cps_lost / nb_sims
        )
    )

    print('{:2.1f}%,{:.1f},{:2.1f}%,{:.1f}'.format(
        100. * att_wins / nb_sims, 1. * att_cps_lost / nb_sims,
        100. * def_wins / nb_sims, 1. * def_cps_lost / nb_sims
        )
    )

def rolls_distribution(nb_dice, tohit):
    nb_sims = 2000
    results = defaultdict(int)
    for i in range(nb_sims):
        hits = 0
        for i in range(nb_dice):
            roll = roll_die()
            if roll <= tohit:
                hits += 1
        results[hits] += 1
    return {
        k: [v, "{:.0f}%".format(100.*v/nb_sims)]
        for k,v in dict(sorted(results.items())).items()
    }
