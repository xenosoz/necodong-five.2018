#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import permutations


def index_to_str(n):
    return '12345!'[n]


def str_to_index(s):
    '''"12345!".index(s): 1.4 micro secs / 6 calls'''
    return ord(s) % 7


def round_score(x, y):
    '''15.1 micro secs / 36 calls'''
    key = 1338084758805431740929
    return ((key >> (x*12 + y*2)) & 0x3) - 1


# (0, 1, 2, 3, 5, 4)
# (0, 1, 3, 5, 2, 4)
# (0, 1, 5, 2, 3, 4)

for seq in permutations(range(6)):
    if all(round_score(a, b) < 0 for a, b in zip(seq, seq[1:] + seq[:1])):
        # NB(xenosoz, 2018): B wins!
        print(seq)
