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


def product(iter_x, iter_y):
    tup_x, tup_y = tuple(iter_x), tuple(iter_y)
    for x in tup_x:
        for y in tup_y:
            yield (x, y)


def shift_0(x, c):
    cycle = (0, 1, 2, 3, 5, 4)
    idx = (cycle.index(x) + c) % len(cycle)
    return cycle[idx]


def shift_1(x, c):
    cycle = (0, 1, 3, 5, 2, 4)
    idx = (cycle.index(x) + c) % len(cycle)
    return cycle[idx]


def shift_2(x, c):
    cycle = (0, 1, 5, 2, 3, 4)
    idx = (cycle.index(x) + c) % len(cycle)
    return cycle[idx]


def multiplex(choice, c):
    '''c in [0, 18)'''
    return [shift_0, shift_1, shift_2][c//6](choice, c%6)


class Widget:
    def __init__(self):
        self.random = LCG(19937-64)  # NB(xenosoz, 2018): I know it's not MT19937-64 for sure :)
        self.solutions = None
        self.scores = None
        self.choice = None
        self.general_frequency = dict()

    def random_choice(self, x):
        pool = tuple(x)
        r = self.random.__next__()
        n = len(pool)
        return pool[r % n]

    def wrap_guess(self, guesses, hands):
        for c in range(18):
            for prob, raw_choice in guesses:
                choice = multiplex(raw_choice, c)
                if choice in hands:
                    yield choice
                    break
            else:
                yield self.random_choice(hands)


    def mode_choice(self, iterable):
        counter = dict()
        for v in iterable:
            counter[v] = counter.get(v, 0) + 1

        max_count = max(counter.values())
        candidates = [v for v, c in counter.items() if c == max_count]
        return self.random_choice(candidates)


    def guess_by_random(self):
        hands = self.mee_hands
        candidates = [(1, self.random_choice(hands))]
        yield from self.wrap_guess(candidates, hands)


    def guess_by_last_history_all(self, mee_you):
        old_games = self.old_games
        history = self.history
        hands = self.mee_hands  # NB(xenosoz, 2018): always choose 'mee' here.

        k = len(history)
        guess = None

        if old_games:
            if k < len(old_games[-1]):
                guess = old_games[-1][k][mee_you]

        if guess is None:
            guess = self.random_choice(range(6))

        candidates = [(1, guess)]
        yield from self.wrap_guess(candidates, hands)


    def guess_by_last_history_mee(self):
        yield from self.guess_by_last_history_all(0)


    def guess_by_last_history_you(self):
        yield from self.guess_by_last_history_all(1)


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


    def guess_by_position_frequency_all(self, pf):
        round_idx = self.round_idx

        z = sum(pf[round_idx])
        good_value = max(pf[round_idx][idx] for idx in range(6))
        candidates = [idx for idx in range(6) if pf[round_idx][idx] == good_value]

        if not candidates or z == 0:
            return []

        return sorted(((pf[round_idx][idx]/float(z), idx) for idx in candidates), reverse=True)


    def guess_by_position_frequency_mee(self):
        hands = self.mee_hands  # NB(xenosoz, 2018): always choose 'mee' here.

        guess = self.guess_by_position_frequency_all(self.mee_position_frequency)
        yield from self.wrap_guess(guess, hands)


    def guess_by_position_frequency_you(self):
        hands = self.mee_hands  # NB(xenosoz, 2018): always choose 'mee' here.

        guess = self.guess_by_position_frequency_all(self.you_position_frequency)
        yield from self.wrap_guess(guess, hands)


    def heat_general_frequency(self, choice_mee_you):
        gf = self.general_frequency

        for n in range(6+1):
            key = (n, tuple(self.mee_hands[6-n:]), None)
            gf[key] = gf.get(key, []) + [choice_mee_you]

            key = (n, None, tuple(self.you_hands[6-n:]))
            gf[key] = gf.get(key, []) + [choice_mee_you]

            key = (n, tuple(self.mee_hands[6-n:]), tuple(self.you_hands[6-n:]))
            gf[key] = gf.get(key, []) + [choice_mee_you]

        self.general_frequency = gf


    def guess_by_hands_all(self):
        gf = self.general_frequency
        history = self.history
        hands = self.mee_hands

        n = len(history)
        mee_h = tuple(mee for mee, you in history)
        you_h = tuple(you for mee, you in history)
        key = (n, mee_h, you_h)
        value = [v for v in gf.get(key, []) if v in hands]

        choice = self.mode_choice(m for m, y in value) if value else self.random_choice(hands)
        yield from self.wrap_guess([(1, choice)], hands)

        choice = self.mode_choice(y for m, y in value) if value else self.random_choice(hands)
        yield from self.wrap_guess([(1, choice)], hands)


    def guess_by_hands_mee(self):
        gf = self.general_frequency
        history = self.history
        hands = self.mee_hands

        n = len(history)
        mee_h = tuple(mee for mee, you in history)
        key = (n, mee_h, None)
        value = [v for v in gf.get(key, []) if v in hands]

        choice = self.mode_choice(m for m, y in value) if value else self.random_choice(hands)
        yield from self.wrap_guess([(1, choice)], hands)

        choice = self.mode_choice(y for m, y in value) if value else self.random_choice(hands)
        yield from self.wrap_guess([(1, choice)], hands)


    def guess_by_hands_you(self):
        gf = self.general_frequency
        history = self.history
        hands = self.mee_hands

        n = len(history)
        you_h = tuple(you for mee, you in history)
        key = (n, None, you_h)
        value = [v for v in gf.get(key, []) if v in hands]

        choice = self.mode_choice(m for m, y in value) if value else self.random_choice(hands)
        yield from self.wrap_guess([(1, choice)], hands)

        choice = self.mode_choice(y for m, y in value) if value else self.random_choice(hands)
        yield from self.wrap_guess([(1, choice)], hands)

    
    def guess_all(self):
        yield from self.guess_by_random()
        yield from self.guess_by_last_history_mee()
        yield from self.guess_by_last_history_you()
        yield from self.guess_by_position_frequency_mee()
        yield from self.guess_by_position_frequency_you()
        yield from self.guess_by_hands_all()
        yield from self.guess_by_hands_mee()
        yield from self.guess_by_hands_you()


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

        self.you_used = sorted(set(you for mee, you in self.history))
        self.you_hands = sorted(set(range(6)) - set(self.you_used))

        self.mee_score = sum(round_score(mee, you) > 0 for mee, you in self.history)
        self.you_score = sum(round_score(you, mee) > 0 for mee, you in self.history)

        # B2: advanced derived info
        self.build_position_frequency()

        #print(self.mee_position_frequency)
        #print(self.you_position_frequency)


        solutions = list(self.guess_all())
        if self.scores is None:
            scores = [0] * len(solutions)
        else:
            scores = self.scores

        good_score = max(scores)
        choices = [solutions[idx] for idx in range(len(scores)) if scores[idx] == good_score]

        if choices:
            choice = self.random_choice(choices)
        else:
            choice = self.random_choice(self.mee_hands)

        self.solutions = solutions
        self.scores = scores
        self.choice = choice

        str_choice = index_to_str(choice)
        return str_choice


    def heat(self, choice_mee_you):
        self.heat_general_frequency(choice_mee_you)

        you = str_to_index(choice_mee_you[1])
        solutions = self.solutions
        scores = self.scores

        for idx, mee in enumerate(solutions):
            scores[idx] += round_score(mee, you)

        self.scores = scores


def think(_hands, _history, _old_games):
    # NB(xenosoz, 2018): framework for re-calculate histories
    w = Widget()

    for game_idx in range(len(_old_games)):
        old_games = _old_games[:game_idx]
        game = _old_games[game_idx]
        hands = set('12345!')

        for history_idx in range(len(game)):
            choice = w.think(sorted(hands), game[:history_idx], old_games)
            w.heat(game[history_idx])
            hands.remove(choice)

    hands = set('12345!')
    for history_idx in range(len(_history)):
        choice = w.think(sorted(hands), _history[:history_idx], _old_games)
        w.heat(_history[history_idx])
        hands.remove(choice)

    choice = w.think(sorted(_hands), _history, _old_games)
    return choice




