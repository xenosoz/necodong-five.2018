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


def expand_gene(s):
    cell = [-1, -1, -1, -1, -1, -1]
    hand = [0, 1, 2, 3, 4, 5]
    for cell_idx in range(len(cell)):
        n = len(cell) - cell_idx
        hand_idx, s = s%n, s//n
        cell[cell_idx] = hand[hand_idx]
        del hand[hand_idx]

    return cell


def round_score(x, y):
    '''15.1 micro secs / 36 calls'''
    key = 1338084758805431740929
    return ((key >> (x*12 + y*2)) & 0x3) - 1


def find_soln(y_gene, x_score, y_score):
    good_score = float('-inf')
    good_genes = []

    for x_gene in range(720):
        xx, x_hand = x_gene, [0, 1, 2, 3, 4, 5]
        yy, y_hand = y_gene, [0, 1, 2, 3, 4, 5]
        x_score = 0

        for n in range(6, 0, -1):
            x_idx, xx = xx%n, xx//n
            y_idx, yy = yy%n, yy//n
            x = x_hand[x_idx]
            y = y_hand[y_idx]
            del x_hand[x_idx]
            del y_hand[y_idx]

            rs = round_score(x, y)
            x_score += rs

        if x_score > good_score:
            good_genes = []
            good_score = x_score

        if x_score == good_score:
            good_genes.append(x_gene)

    return good_genes


def think(hands, history, old_games):
    y_gene = 0
    x_gene = find_soln(y_gene, 0, 0)[0]
    choice = index_to_str(expand_gene(x_gene)[len(history)])
    return choice


