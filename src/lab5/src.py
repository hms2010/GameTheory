import math
import random
from scipy.optimize import linprog
from c import *

def get_row_by_index(matrix, index):
    return matrix[index]

def get_column_by_index(matrix, index):
    return [matrix[i][index] for i in range(len(matrix))]

def transpose_matrix(matrix):
    return [get_column_by_index(matrix, i) for i in range(len(matrix[0]))]

def is_equal_with_eps(a, b, eps = 10**-6):
    return (abs(a - b) < eps)

def get_min_indexes_list(arr, eps = 10**-6):
    min_i = []
    min_el = min(arr)
    for i in range(len(arr)):
        if is_equal_with_eps(arr[i], min_el, eps):
            min_i.append(i)
    return min_i

def simplex_method(C):
    A = transpose_matrix(C)
    for i in range(len(A)):
        for j in range(len(A[0])):
            A[i][j] *= -1
    b = [-1] * len(A)
    c = [1] * len(A[0])
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None) for i in range(len(c))])
    cost = 1 / res.fun
    strats = [i * cost for i in res.x]
    return strats

def get_cur_opt_cost(A, x):
    res = [0] * len(A[0])
    for i in range(len(A[0])):
        for j in range(len(A)):
            res[i] += x[j] * A[j][i]
    return res

def get_cur_strat_opt(alpha, prev, cur_opt):
    res = [0] * len(prev)
    for i in range(len(prev)):
        res[i] += (1 - alpha)*prev[i] + alpha*cur_opt[i]
    return res

def check_all_cost_equal(cur_cost, eps):
    for i in range(len(cur_cost)):
        for j in range(i, len(cur_cost)):
            if not is_equal_with_eps(cur_cost[i], cur_cost[j], eps):
                return False
        return True

def monotonous_method(C, eps = 10**-6):
    print("*" * 128)
    print("Game solving with monotonous method...")
    cur_strat, cur_cost = [1] + [0] * (len(C) - 1), get_row_by_index(C, 0)
    N = 0
    while True:
        N += 1
        print("Current iteration: {:d}".format(N))
        print("    Current strategy:", cur_strat)
        print("    Current cost:    ", cur_cost)
        if check_all_cost_equal(cur_cost, eps):
            print("Game solution was found.")
            print("*" * 128)
            return cur_strat, min(cur_cost)
        J = sorted(get_min_indexes_list(cur_cost, eps))
        print("    J:", J)
        subgame = []
        for i in range(len(C)):
            line = []
            for j in J:
                line.append(C[i][j])
            subgame.append(line)
        cur_opt_strat = simplex_method(subgame)
        print("    Current optimal strategy:", cur_opt_strat)
        cur_opt_cost = get_cur_opt_cost(C, cur_opt_strat)
        print("    Current optimal cost:    ", cur_opt_cost)
        subgame = [cur_cost, cur_opt_cost]
        subgame_cost = simplex_method(subgame)
        alpha = subgame_cost[1]
        print("    Aplha = ", alpha)
        print("-" * 128)
        if is_equal_with_eps(0, alpha, eps):
            print("Game solution was found.")
            print("*" * 128)
            return cur_strat, min(cur_cost)

        cur_strat = get_cur_strat_opt(alpha, cur_strat, cur_opt_strat)
        cur_cost = get_cur_strat_opt(alpha, cur_cost, cur_opt_cost)

def main():
    accuracy = int(input("Enter current accuracy: "))
    print("Cost matrix C:")
    for line in C:
        print(line)
    print("-" * 128)
    x, cost = monotonous_method(C, 10**(-accuracy))
    print("Player A strategy x =", [round(i, accuracy) for i in x])
    print("Game cost = ", round(cost, accuracy))

if __name__ == '__main__':
    main()

