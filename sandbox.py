#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def str_to_index(s):
    '''"!12345".index(s)'''
    x = ord(s) ^ 0x30
    x = (x>>4) ^ (x&0xF)
    return x

for s in '!12345':
    print(str_to_index(s))

