#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from importlib import import_module

lhs_module = import_module('bots.constant-A')
rhs_module = import_module('dummies.constant-A')

candidates = '12345!'

lhs_hand = list(candidates)
rhs_hand = list(candidates)
lhs_hist = []
rhs_hist = []

while lhs_hand and rhs_hand:
    lhs_choice = lhs_module.think(lhs_hand, lhs_hist, [])
    rhs_choice = rhs_module.think(rhs_hand, rhs_hist, [])

    lhs_hand.remove(lhs_choice)
    rhs_hand.remove(rhs_choice)

    lhs_hist.append([lhs_choice, rhs_choice])
    rhs_hist.append([rhs_choice, lhs_choice])

    print(lhs_choice, rhs_choice)


