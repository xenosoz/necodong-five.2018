#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stadium
import sys
from pathlib import Path

bot_name = 'bots.constant-A' if len(sys.argv) <= 1 else sys.argv[1]
winn, lose, draw = 0, 0, 0

for p in Path('dummies').glob('*.py'):
    dummy_name = '.'.join(p.parts[:-1] + (p.stem,))
    bot_score, dummy_score = stadium.play_a_game(bot_name, dummy_name, debug=False)
    winn += (bot_score > dummy_score)
    lose += (bot_score < dummy_score)
    draw += (bot_score == dummy_score)

print(bot_name)
print('=' * len(bot_name))
print('winn\tlose\tdraw')
print(winn, lose, draw, sep='\t')

