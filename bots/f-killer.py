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


def permutations(iterable):
    '''TAOCP pp.42 Algorithm P'''
    pool = list(iterable)
    n = len(pool)

    # P1. Initialize.
    c = [0] * n
    o = [1] * n

    while n:
        # P2. Visit.
        yield list(pool)
        
        # P3. Prepare for change.
        s = 0
        for j in reversed(range(0, n)):
            # P4. Ready to change?
            q = c[j] + o[j]

            if q >= 0:
                if j >= q:
                    # P5. Change.
                    lhs = j - c[j] + s
                    rhs = j - q + s
                    pool[lhs], pool[rhs] = pool[rhs], pool[lhs]
                    c[j] = q
                    break

                # P6. Increase s.
                if j == 0: return
                s += 1

            # P7. Switch direction.
            o[j] = -o[j]


def random_guess():
    pass


def frequency_analysis():
    pass


def history_matching():
    pass


def last_p(hands, history, old_games):
    if old_games:
        last_game = old_games[-1]
        last_game_x = [x for x, y in last_game]
        last_game_y = [y for x, y in last_game]

    return hands[0]


def think(hands, history, old_games):
    pass


    # (0, 4, 2, 5, 3, 1)
    # (0, 4, 3, 2, 5, 1)
    # (0, 4, 5, 3, 2, 1)


for x in permutations([1,2,3]):
    print(x)






