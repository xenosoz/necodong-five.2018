#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from importlib import import_module
from itertools import product


def round_score(mine, yours):
    winn, lose, draw = 1, -1, 0

    if mine == '1':
        return {'1': draw, '2': lose, '3': lose, '4': lose, '5': winn, '!': winn}[yours]

    if mine == '2':
        return {'1': winn, '2': draw, '3': lose, '4': lose, '5': lose, '!': lose}[yours]

    if mine == '3':
        return {'1': winn, '2': winn, '3': draw, '4': lose, '5': lose, '!': winn}[yours]

    if mine == '4':
        return {'1': winn, '2': winn, '3': winn, '4': draw, '5': lose, '!': lose}[yours]

    if mine == '5':
        return {'1': lose, '2': winn, '3': winn, '4': winn, '5': draw, '!': winn}[yours]

    if mine == '!':
        return {'1': lose, '2': winn, '3': lose, '4': winn, '5': lose, '!': draw}[yours]

    assert False


def test_round_score():
    candidates = '12345!'
    for lhs, rhs in product(candidates, candidates):
        assert lhs != rhs or round_score(lhs, rhs) == round_score(rhs, lhs)
        assert round_score(lhs, rhs) + round_score(rhs, lhs) == 0


def play_a_set(lhs_name, rhs_name):
    print(' v ' + lhs_name)
    print('    v ' + rhs_name)

    lhs_module = import_module(lhs_name)
    rhs_module = import_module(rhs_name)
    candidates = '12345!'

    lhs_hand = list(candidates)
    rhs_hand = list(candidates)

    lhs_hist = []
    rhs_hist = []

    lhs_score = 0
    rhs_score = 0

    while lhs_hand and rhs_hand:
        lhs_choice = lhs_module.think(lhs_hand, lhs_hist, [])
        rhs_choice = rhs_module.think(rhs_hand, rhs_hist, [])

        lhs_hand.remove(lhs_choice)
        rhs_hand.remove(rhs_choice)

        lhs_hist.append([lhs_choice, rhs_choice])
        rhs_hist.append([rhs_choice, lhs_choice])

        lhs_delta = round_score(lhs_choice, rhs_choice)
        rhs_delta = round_score(rhs_choice, lhs_choice)

        print(' [ '[lhs_delta] + lhs_choice + ' ] '[lhs_delta], end='')
        print(' [ '[rhs_delta] + rhs_choice + ' ] '[rhs_delta], end='')
        print()

        lhs_score += lhs_delta
        rhs_score += rhs_delta
        if lhs_score >= 3 or rhs_score >= 3:
            return (lhs_score, rhs_score)

    return (lhs_score, rhs_score)


if __name__ == '__main__':
    test_round_score()
    lhs_name = 'bots.constant-A'
    rhs_name = 'dummies.constant-B3'
    
    r = play_a_set(lhs_name, rhs_name)
    print(r)

