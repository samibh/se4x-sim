# Space Empires 4X combat simulation library

This library provides a fight simulator for the boardgame **Space Empires: 4X**
and its extensions **Close Encounters** and **Replicators**.


### Requirements

- Needs python 3 to run.
- See the links in [credits](#credits) to download updated rule books from the official website.

### Status and expectations

This is still a very rough initial version. Hopefully it gives accurate results, but
there may be hidden bugs, edge cases or mistakes lurking.

It is a hobby project, hastily written on holiday between two play sessions.
Don't expect high code quality (yet), but feel free to submit PRs if you have
improvements to suggest, I still use and maintain it.

Copyright (c) 2018 Sami Ben Hatit, licensed under the MIT license.

## Overview

### fight()

`fight(att_fleet, att_upgrades, def_fleet, def_upgrades, verbose=False)`

Simulates a single fight between the attacking fleet `att_fleet`, equipped with
the upgrades `att_upgrades` against teh defending fleet `def_fleet`, equipped
with the upgrades `def_upgrades`.

Input
- `att_fleet` list of ships in the attacking fleet e.g. `[S_BOARD,S_BOARD,S_BOARD]`
- `att_upgrades` upgrades for all ships in the attacking fleet
- `def_fleet` list of ships in the defending fleet e.g. `[S_CRUISER,S_CRUISER]`
- `def_upgrades` upgrades for all ships in the defending fleet
- `verbose` if True, output debugging log with detailed rolls and ships state

Output
a tuple `(nb_att, nb_def, next_ships, att_cp_lost, def_cp_lost)`
- `nb_att` number of attacking ships left after the fight
- `nb_def` number of defending ships left after the fight
- `next_ships` ships left after the fight
- `att_cp_lost` CP value of ships lost by attacker
- `def_cp_lost` CP value of ships lost by defender

### Upgrades()

Class describing the upgrades and powers applicable to a ship or a fleet

```python
Upgrades(attack=0, defense=0, boarding=0, security=0, cloaking=0, fighter=0, tactics=0,
         immortal=False, giant=False, hivemind=False)
```

### Ships

```python
S_SCOUT = {'name':'Scout', 'cost':6, 'prio':5, 'att':3, 'def':0, 'size':1}
S_DESTRO = {'name':'Destroyer', 'cost':9, 'prio':4, 'att':4, 'def':0, 'size':1}
S_CRUISER = {'name':'Cruiser', 'cost':12, 'prio':3, 'att':4, 'def':1, 'size':2}
S_BC = {'name':'Battlecruiser', 'cost':15, 'prio':2, 'att':5, 'def':1, 'size':2}
S_BB = {'name':'Battleship', 'cost':20, 'prio':1, 'att':5, 'def':2, 'size':3}
S_DREAD = {'name':'Dreadnaught', 'cost':24, 'prio':1, 'att':6, 'def':3, 'size':3}
S_TITAN = {'name':'Titan', 'cost':32, 'prio':1, 'att':7, 'def':3, 'size':5}
S_BOARD = {'name':'Boarding', 'cost':12, 'prio':6, 'att':5, 'def':0, 'size':2}
S_CARRIER = {'name':'Carrier', 'cost':5, 'prio':5, 'att':3, 'def':1, 'size':1}
S_TRANSPORT = {'name':'Transport', 'cost':6, 'prio':5, 'att':1, 'def':1, 'size':1}

S_BASE = {'name':'Base', 'cost':12, 'prio':1, 'att':7, 'def':2, 'size':3}
S_SHIPYARD = {'name':'Shipyard', 'cost':6, 'prio':3, 'att':3, 'def':1, 'size':1}

S_RAIDER_NOCLOAK = {'name':'Raider', 'cost':12, 'prio':4, 'att':4, 'def':0, 'size':2}
S_RAIDER_CLOAKED = {'name':'Raider (clkd)', 'cost':12, 'prio':1, 'att':5, 'def':0, 'size':2}

S_FIGHTER = {'name':'Fighter', 'cost':5, 'prio':2, 'att':5, 'def':0, 'size':1}

S_SWEEPER = {'name':'Sweeper', 'cost':6, 'prio':5, 'att':1, 'def':0, 'size':1}

S_DDX = {'name':'DDX', 'cost':9, 'prio':4, 'att':4, 'def':0, 'size':1}

S_ALIENB = {'name':'Alien B', 'cost':0, 'prio':2, 'att':6, 'def':2, 'size':1}
S_ALIENC = {'name':'Alien C', 'cost':0, 'prio':3, 'att':5, 'def':2, 'size':1}
S_ALIEND = {'name':'Alien D', 'cost':0, 'prio':4, 'att':4, 'def':1, 'size':1}

S_FLAGSHIP = {'name':'HMS Jeff', 'cost':0, 'prio':2, 'att':4, 'def':1, 'size':3}

# Cloaking geniuses
S_SCOUT_CG = {'name':'Scout clkd', 'cost':6, 'prio':1, 'att':3, 'def':0, 'size':1}
S_DESTRO_CG = {'name':'Destroyer clkd', 'cost':9, 'prio':1, 'att':4, 'def':0, 'size':1}
S_CRUISER_CG = {'name':'Cruiser clkd', 'cost':12, 'prio':1, 'att':4, 'def':1, 'size':2}

# Insectoids
S_BOARD_INS = {'name':'Boarding (insectoids)', 'cost':12, 'prio':6, 'att':5, 'def':0, 'size':1}
```

### TODO

- tests
- improve documentation
- additional rule support
- support of per ship upgrades instead of per fleet upgrades
- support for more racial powers in Upgrades instead of designing different ships
- support for cloaking counter-detection instead of designing different ships
- transport upgrades
- smarter targeting, the current method is very straightforward, in this order: wounded ships, boarding, 1 hp ships, 2 hp ships, anything else


## Usage

Example of use (a jupyter notebook sample is included):

```python
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
```


## Credits

**[Space Empires: 4X](https://www.gmtgames.com/p-533-space-empires-3rd-printing.aspx)** is an excellent game by:  
DESIGNER: Jim Krohn  
DEVELOPER: Martin Scott  
ART DIRECTOR/PACKAGE ART: Rodger B. MacGowan  
MAP & COUNTER ART: Mark Simonitch  
PRODUCERS: Andy Lewis, Gene Billingsley, Mark Simonitch, Rodger MacGowan, & Tony Curtis

**[Space Empires: Close Encounters](https://www.gmtgames.com/p-687-space-empires-close-encounters-2nd-printing.aspx)** is the also excellent first expansion by:  
DESIGNER: Jim Krohn  
DEVELOPER: Oliver Upshaw  
COVER ART: Eric Williams  
ART DIRECTOR, PACKAGING: Rodger B. MacGowan  
COUNTER ART: Mark Simonitch  
PRODUCERS: Andy Lewis, Gene Billingsley, Mark Simonitch, Rodger MacGowan, & Tony Curtis

**[Space Empires: Replicators](https://www.gmtgames.com/p-468-space-empires-replicators.aspx)** is the second, still excellent, expansion by:  
DESIGNER: Jim Krohn  
DEVELOPER: Oliver Upshaw  
TILE ART: Michael Evans  
PRODUCERS: Gene Billingsley, Tony Curtis, Andy Lewis, Rodger MacGowan, Mark Simonitch
