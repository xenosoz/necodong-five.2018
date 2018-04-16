#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# NB(2018, xenosoz): Please feel free to contact me: xenosoz.hwang@gmail.com
#   Let's live a good life with me. We might be good friends!
#

def index_to_str(n):
    return '12345!'[n]


def str_to_index(s):
    '''"12345!".index(s): 1.4 micro secs / 6 calls'''
    return ord(s) % 7


def round_score(x, y):
    '''15.1 micro secs / 36 calls'''
    key = 1338084758805431740929
    return ((key >> (x*12 + y*2)) & 0x3) - 1


def build_future(present):
    lp = len(present)
    lblank = 6 - lp

    combi = 1
    for c in range(lblank):
        combi *= c+1

    for s in range(combi):
        cell = [None, None, None, None, None, None]
        cell[:lp] = present

        hand = sorted(set(range(6)) - set(present))

        for cell_idx in range(lblank):
            n = lblank - cell_idx
            hand_idx, s = s%n, s//n
            cell[cell_idx + lp] = hand[hand_idx]
            del hand[hand_idx]

        yield cell


def find_killers(y_cell):
    good_score = float('-inf')
    good_cells = []

    for x_cell in build_future([]):
        x_score = 0

        for x, y in zip(x_cell, y_cell):
            rs = round_score(x, y)
            x_score += rs
            if x_score <= -3:
                x_score = float('-inf')

        if x_score > good_score:
            good_cells.clear()
            good_score = x_score

        if x_score == good_score:
            good_cells.append(x_cell)

    return good_cells


def think(hands, history, old_games):
    x_cell_part = [str_to_index(x) for x, y in history]
    y_cell = [str_to_index(y) for x, y in old_games[-1]] if old_games else [0, 1, 2, 3, 4, 5]

    killers = find_killers(y_cell)
    choice = index_to_str(killers[0][len(history)])
    return choice

