#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stadium
from pathlib import Path


def eval_bot(bot_name):
    winn, lose, draw = 0, 0, 0

    for p in Path('dummies').glob('*.py'):
        dummy_name = '.'.join(p.parts[:-1] + (p.stem,))
        bot_score, dummy_score = stadium.play_a_game(bot_name, dummy_name, debug=False)
        winn += (bot_score > dummy_score)
        lose += (bot_score < dummy_score)
        draw += (bot_score == dummy_score)

    return (winn, lose, draw)


if __name__ == '__main__':
    import sys
    bot_name = 'bots.constant-A' if len(sys.argv) <= 1 else sys.argv[1]

    print(bot_name)
    print('=' * len(bot_name))

    winn, lose, draw = eval_bot(bot_name)
    print('winn\tlose\tdraw')
    print(winn, lose, draw, sep='\t')

