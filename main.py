from itertools import product
from itertools import izip
import random


def decode_color(number):
    return {0: 'Y', 1: 'B', 2: 'R', 3: 'G', 4: 'W', 5: 'K'}.get(number, number) 


def decode_colors(numbers):
    return ''.join(map(decode_color, numbers))


def first_move(npositions, ncolors):
    #    first = random.randint(0, ncolors - 1)
    #    second = random.randint(0, ncolors - 1)
    first = 0
    second = 1
    result = []
    for i in range(npositions):
        if i < npositions / 2:
            result.append(first)
        else:
            result.append(second)
    return result


def all_permutation(npositions, ncolors):
    return product(range(ncolors), repeat=npositions)


def idx(iterable, value):
    for i, x, in enumerate(iterable):
        if x == value:
            return i
    return None


def response(secret, test):
    k, w = 0, 0
    secret = list(secret[:])
    test = list(test[:])

    for i, (s, t) in enumerate(izip(secret, test)):
        if s == t:
            k += 1
            secret[i] = None
            test[i] = None

#    return k, sum([min(secret.count(j), test.count(j)) for j in xrange(len(secret))]) - k

    for i, s in enumerate(secret):
        if s is None:
            continue
        where = idx(test, s)
        if where is not None:
            w += 1
            secret[i] = None
            test[where] = None
    return k, w


def compute_possibilities(possibilities, test, hint):
    return set(p for p in possibilities if response(p, test) == hint)


NCOLORS = 6
NPOSITIONS = 4

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Solve Masterming game')
    parser.add_argument('--secret', help='the secret if you know it')
    args = parser.parse_args()

    if args.secret is not None:
        secret = map(int, list(args.secret))
        print "the secret is %s" % secret
    else:
        secret = None

    possibilities = set(all_permutation(NPOSITIONS, NCOLORS))
    results = [(right, wrong) for right in range(5) for wrong in range(5 - right) if not (right == 3 and wrong == 1)]

    first = True

    while True:
        if first:
            best_test = first_move(NPOSITIONS, NCOLORS)
        else:
            best_test = None
            nbest_test = 100000000000

            for test in possibilities:
                nremaining = 0
                iterable = results
                if len(possibilities) <= len(results):
                    iterable = [response(possible_secret, test) for possible_secret in possibilities]
                for hint in iterable:
                    n = len(compute_possibilities(possibilities, test, hint))
                    if n > nremaining:
                        nremaining = n
                if nremaining < nbest_test:
                    best_test = test
                    nbest_test = nremaining
        first = False
        print "move: ", decode_colors(best_test)
        while True:
            if secret:
                real_response = response(secret, best_test)
            else:
                real_response = tuple(map(int, raw_input('enter response:').split(" ")))
            temp = compute_possibilities(possibilities, best_test, real_response)
            if len(temp) > 0:
                possibilities = temp
                break
            else:
                print "wrong response, no more possibilities, retry"
        nbest_test = len(possibilities)
        print "response: ", real_response
        print "remaining possibilities: ", nbest_test
        if nbest_test == 1:
            print "win, solution", decode_colors(list(possibilities)[0])
            break
