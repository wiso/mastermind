from itertools import permutations, product
from itertools import izip
import random

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

NCOLORS = 8
NPOSITIONS = 4

secret = [random.randint(0, NCOLORS-1) for _ in xrange(NPOSITIONS)]
secret = [1, 2, 3, 4]
print "secret: ", secret

possibilities = set(all_permutation(NPOSITIONS, NCOLORS))
results = [(right, wrong) for right in range(5) for wrong in range(5 - right) if not (right == 3 and wrong == 1)]


#for p in possibilities:
#    print p, response(secret, p)

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
                print "using"
            for hint in iterable:
                n = len(compute_possibilities(possibilities, test, hint))
                if n > nremaining:
                    nremaining = n
            if nremaining < nbest_test:
                best_test = test
                nbest_test = nremaining
    first = False
    print best_test
    print "move: ", ''.join(map(str, best_test))
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
    print "remaining possibilities: ", nbest_test, possibilities
    if nbest_test == 1:
        print "win"
        break
