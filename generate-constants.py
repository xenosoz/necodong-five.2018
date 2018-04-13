#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import call
import math

def lei(n):
    if n == 0:
        return 'A'
    return chr(ord('B') + int(math.log10(n))) + str(n)


for seq in range(1, 6*5*4*3*2*1):
    lei_seq = lei(seq)
    call(['ln', '-s', 'constant-A.py', 'bots/constant-{}.py'.format(lei_seq)])

