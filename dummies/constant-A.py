#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def think(hands, history, old_games):
    seq = int('0' + __name__.split('.')[-1].split('-')[1][1:])
    for _, d in zip(history, range(6, 1, -1)):
        seq //= d
    
    return hands[seq % len(hands)]


def go():
    cand = '12345!'
    a_hand = list(cand)
    a_hist = []
    while a_hand:
        a_choice = think(a_hand, a_hist, [])
        print(a_choice, end='')
        a_hist.append(a_choice)
        a_hand.remove(a_choice)
    print()
