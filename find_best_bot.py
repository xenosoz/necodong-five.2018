#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from eval_bot import eval_bot
from pathlib import Path
import sys

good_score = -1
good_names = []

for p in Path('dummies').glob('*.py'):
    dummy_name = '.'.join(p.parts[:-1] + (p.stem,))
    winn, lose, draw = eval_bot(dummy_name)

    print(dummy_name, (winn, lose, draw), file=sys.stderr)

    score = winn * 3 + draw
    if score > good_score:
        good_score = score
        good_names = []

    if score == good_score:
        good_names.append(dummy_name)

print(good_score)
print(good_names)

