#!/usr/bin/env python
import sys
import json
from operator import itemgetter
import re

stat_mappings = {
    'name': 'disp_name',
    'ad': 'dam_base',
    'scaling_ad': 'dam_lvl',
    'armor': 'arm_base',
    'scaling_armor': 'arm_lvl',
    'attack_speed': 'as_base',
    'scaling_base_attack_speed': 'as_lvl',
    'health': 'hp_base',
    'scaling_health': 'hp_lvl',
    'health_regen': 'hp5_base',
    'scaling_health_regen': 'hp5_lvl',
    'mana': 'mp_base',
    'scaling_mana': 'mp_lvl',
    'mana_regen': 'mp5_base',
    'scaling_mana_regen': 'mp5_lvl',
    'move_speed': 'ms',
    'mr': 'mr_base',
    'scaling_mr': 'mr_lvl',
    'range': 'range',
}

if __name__ == '__main__':
    infile = open(sys.argv[1])
    champs = json.load(infile)
    champs.sort(key=itemgetter('disp_name'))
    for champ in champs:
        def print_stat(name, key):
            outfile.write(f"    {name} = {repr(champ[key])}\n")
        champ['as_lvl'] /= 100  # convert from percent to float
        name = re.sub('\W', '', champ['disp_name'])
        outfile = open(f'champions/{name}.py', 'w')
        outfile.write("from champion import Champion\n\n\n")
        outfile.write(f"class {name}(Champion):\n")
        for stat, key in stat_mappings.items():
            print_stat(stat, key)
