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


def LCG(seed):
    m = 2**32
    a = 1664525
    c = 1013904223
    
    x = seed
    while True:
        x = (a * x + c) % m
        yield x


def shift_0(x, c):
    cycle = (0, 4, 2, 5, 3, 1)
    idx = (cycle.index(x) + c) % len(cycle)
    return cycle[idx]


def shift_1(x, c):
    cycle = (0, 4, 3, 2, 5, 1)
    idx = (cycle.index(x) + c) % len(cycle)
    return cycle[idx]


def shift_2(x, c):
    cycle = (0, 4, 5, 3, 2, 1) 
    idx = (cycle.index(x) + c) % len(cycle)
    return cycle[idx]


class Widget:
    def __init__(self):
        self.random = LCG(19937-64)  # NB(xenosoz, 2018): I know it's not MT19937-64 for sure :)

    def random_choice(self, x):
        pool = tuple(x)
        r = self.random.__next__()
        n = len(pool)
        return pool[r % n]


    def random_guess(self):
        pass


    def frequency_analysis(self):
        pass


    def history_matching(self):
        pass


    def build_position_frequency(self):
        '''self.old_games -> self.[mee|you]_position_frequency'''
        old_games = self.old_games

        # pf[position][number] := count
        mee_pf = [[0] * 6 for x in range(6)]  
        you_pf = [[0] * 6 for x in range(6)]

        for game in old_games:
            for idx, (mee, you) in enumerate(game):
                mee_pf[idx][mee] += 1
                you_pf[idx][you] += 1

        self.mee_position_frequency = mee_pf
        self.you_position_frequency = you_pf


    def mee_guess(self):
        round_idx = self.round_idx
        mee_hands = self.mee_hands
        mee_pf = self.mee_position_frequency

        good_value = max(mee_pf[round_idx][idx] for idx in mee_hands)
        candidates = [idx for idx in mee_hands if mee_pf[round_idx][idx] == good_value]

        if not candidates:
            return None

        return self.random_choice(candidates)


    def think(self, hands, history, old_games):
        # A: given condition
        self.str_hands = hands
        self.str_history = history
        self.str_old_games = old_games

        # B1: basic derived info
        self.round_idx = len(history)
        self.history = [(str_to_index(mee), str_to_index(you)) for mee, you in self.str_history]
        self.old_games = [[(str_to_index(mee), str_to_index(you)) for mee, you in game] for game in self.str_old_games]

        self.mee_hands = [str_to_index(hand) for hand in self.str_hands]
        self.mee_used = sorted(set(range(6)) - set(self.mee_hands))

        self.you_used = sorted(set(str_to_index(you) for mee, you in history))
        self.you_hands = sorted(set(range(6)) - set(self.you_used))

        # B2: advanced derived info
        self.build_position_frequency()

        print(self.mee_position_frequency)
        print(self.you_position_frequency)


        choice = self.mee_guess()
        str_choice = index_to_str(choice)
        print('choice: ', str_choice)

        return str_choice



def think(hands, history, old_games):
    w = Widget()
    return w.think(hands, history, old_games)


