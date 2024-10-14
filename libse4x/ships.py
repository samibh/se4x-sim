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

S_SC           = {'name':'Scout'        , 'cost': 6, 'prio':5, 'att':3, 'def':0, 'size':1}
S_SCOUT        = S_SC
S_DD           = {'name':'Destroyer'    , 'cost': 9, 'prio':4, 'att':4, 'def':0, 'size':1}
S_DESTRO       = S_DD
S_CA           = {'name':'Cruiser'      , 'cost':12, 'prio':3, 'att':4, 'def':1, 'size':2}
S_CRUISER      = S_CA
S_BC           = {'name':'Battlecruiser', 'cost':15, 'prio':2, 'att':5, 'def':1, 'size':2}
S_BB           = {'name':'Battleship'   , 'cost':20, 'prio':1, 'att':5, 'def':2, 'size':3}
S_DN           = {'name':'Dreadnaught'  , 'cost':24, 'prio':1, 'att':6, 'def':3, 'size':3}
S_DREAD        = S_DN
S_TITAN        = {'name':'Titan'        , 'cost':32, 'prio':1, 'att':7, 'def':3, 'size':5}

S_BD           = {'name':'Boarding'     , 'cost':12, 'prio':6, 'att':5, 'def':0, 'size':2}
S_BOARD        = S_BD
S_CV           = {'name':'Carrier'      , 'cost': 5, 'prio':5, 'att':3, 'def':1, 'size':1}
S_CARRIER      = S_CV
S_F            = {'name':'Fighter'      , 'cost': 5, 'prio':2, 'att':5, 'def':0, 'size':1}
S_FIGHTER      = S_F
S_BV           = {'name':'Carrier adv'  , 'cost': 5, 'prio':2, 'att':5, 'def':1, 'size':3}

S_T            = {'name':'Transport'    , 'cost': 6, 'prio':5, 'att':1, 'def':1, 'size':1}
S_TRANSPORT    = S_T
S_MILITIA      = {'name':'Militia'      , 'cost': 0, 'prio':5, 'att':5, 'def':0, 'size':1, 'ground': True}
S_INFANTRY     = {'name':'Infantry'     , 'cost': 2, 'prio':4, 'att':5, 'def':1, 'size':1, 'ground': True}
S_MARINE_ATT   = {'name':'Marines (att)', 'cost': 3, 'prio':3, 'att':6, 'def':1, 'size':2, 'ground': True}
S_MARINE_DEF   = {'name':'Marines (def)', 'cost': 3, 'prio':4, 'att':5, 'def':1, 'size':2, 'ground': True}
S_HI_ATT       = {'name':'Hvy inf (att)', 'cost': 3, 'prio':4, 'att':4, 'def':2, 'size':2, 'ground': True}
S_HI_DEF       = {'name':'Hvy inf (def)', 'cost': 3, 'prio':3, 'att':6, 'def':2, 'size':2, 'ground': True}
S_GRAV         = {'name':'Grav Armor'   , 'cost': 4, 'prio':3, 'att':6, 'def':2, 'size':2, 'ground': True}

S_BASE         = {'name':'Base'         , 'cost':12, 'prio':1, 'att':7, 'def':2, 'size':3}
S_SY           = {'name':'Shipyard'     , 'cost': 6, 'prio':3, 'att':3, 'def':1, 'size':1}
S_SHIPYARD     = S_SY

S_RAIDER_NOCLK = {'name':'Raider'       , 'cost':12, 'prio':4, 'att':4, 'def':0, 'size':2}
S_RAIDER_CLK   = {'name':'Raider (clkd)', 'cost':12, 'prio':1, 'att':5, 'def':0, 'size':2}

S_SW           = {'name':'Sweeper'      , 'cost': 6, 'prio':5, 'att':1, 'def':0, 'size':1}
S_SWEEPER      = S_SW

S_DDX          = {'name':'DDX'          , 'cost': 9, 'prio':4, 'att':4, 'def':0, 'size':1}

S_ALIENB       = {'name':'Alien B'      , 'cost': 0, 'prio':2, 'att':6, 'def':2, 'size':1}
S_ALIENC       = {'name':'Alien C'      , 'cost': 0, 'prio':3, 'att':5, 'def':2, 'size':1}
S_ALIEND       = {'name':'Alien D'      , 'cost': 0, 'prio':4, 'att':4, 'def':1, 'size':1}

S_FLAGSHIP     = {'name':'HMS Jeff'     , 'cost': 0, 'prio':2, 'att':4, 'def':1, 'size':3}
S_ADVFLAG      = {'name':'Enterpris'    , 'cost': 0, 'prio':1, 'att':5, 'def':3, 'size':3}

#Insectoids
S_BOARD_INS    = {'name':'Boarding (insectoids)', 'cost':12, 'prio':6, 'att':5, 'def':0, 'size':1}

# Cloaking geniuses
S_SCOUT_CG     = {'name':'Scout clkd'    , 'cost': 6, 'prio':1, 'att':3, 'def':0, 'size':1}
S_DESTRO_CG    = {'name':'Destroyer clkd', 'cost': 9, 'prio':1, 'att':4, 'def':0, 'size':1}
S_CRUISER_CG   = {'name':'Cruiser clkd'  , 'cost':12, 'prio':1, 'att':4, 'def':1, 'size':2}


