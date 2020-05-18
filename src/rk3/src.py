from game_params import *
from math import factorial
from fractions import Fraction

def is_supperadditive(chars):
    for i in chars:
        for j in chars:
            if (i & j) == 0:
                if chars[i | j] < (chars[i] + chars[j]):
                    return False
    return True

def is_convex(chars):
    for i in chars:
        for j in chars:
            if (chars[i | j] + chars[i & j]) < (chars[i] + chars[j]):
                return False
    return True

def sets_power(s):
    res = 0
    while s:
        res += s & 0x01
        s >>= 1
    return res

def shapley_value(chars):
    vec = []
    for i in range(N):
        res = Fraction(0)
        for coal in chars:
            if (coal & 2**i) == 0:
                continue
            coal_power = sets_power(coal)
            res += (factorial(coal_power - 1) *
                        factorial(N - coal_power) *
                            (chars[coal] - chars[coal & ~(2**i)]))
        res /= factorial(N) 
        vec.append(res)
    return vec

def check_group_rationalization(vec):
    return sum(vec) == chars[2**N - 1]

def check_individual_rationalization(vec):
    for i in range(N):
        if vec[i] < chars[2**i]:
            return False
    return True 

def main():
    if is_supperadditive(chars):
        print("Game is supperadditive")
    else:
        print("Game isn't supperadditive")

    if is_convex(chars):
        print("Game is convex")
    else:
        print("Game isn't convex")

    shapley_vector = shapley_value(chars)
    print("Shapley vector: [{:s}]".format(", ".join(["{:.2f}".format(float(i)) for i in shapley_vector])))

    if check_group_rationalization(shapley_vector):
        print("Group rationalization: OK")
    else:
        print("Group rationalization: FAILED")

    if check_individual_rationalization(shapley_vector):
        print("Individual rationalization: OK")
    else:
        print("Individual rationalization: FAILED")

if __name__ == "__main__":
    main()