#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def solve(a, b, c):
    return tuple([(a*i+b)%c for i in range(6)]) == (0, 4, 2, 5, 3, 1)


def go():
    for c in range(1, 20000):
        print(c)
        for a in range(0, c):
            for b in range(0, c):
                if solve(a, b, c):
                    print(a, b, c)
                    return
                    

go()

