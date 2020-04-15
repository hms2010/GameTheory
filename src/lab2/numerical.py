import math
from fractions import Fraction
import random

def get_rand_max_index(arr):
    max_i = []
    max_el = max(arr)
    i = arr.index(max_el)
    max_i.append(i)
    while i < len(arr):
        try:
            i = arr.index(max_el, i + 1)
            max_i.append(i)
        except ValueError:
            break
    return random.choice(max_i)

def get_rand_min_index(arr):
    min_i = []
    min_el = min(arr)
    i = arr.index(min_el)
    min_i.append(i)
    while i < len(arr):
        try:
            i = arr.index(min_el, i + 1)
            min_i.append(i)
        except ValueError:
            break
    return random.choice(min_i)

def get_row_by_index(matrix, index):
    return matrix[index]

def get_column_by_index(matrix, index):
    return [matrix[i][index] for i in range(len(matrix))]

def get_max_index(arr):
    return arr.index(max(arr))

def get_min_index(arr):
    return arr.index(min(arr))

def vector_addition(a, b):
    return [i + j for i, j in zip(a, b)]

def brown_robinson_method(C, eps):
    m = len(C)    # A player strategies: strategy row consists of win of A
    n = len(C[0]) # B player strategies: strategy column consist of loss of B

    x = m * [0]
    y = n * [0]

    curr_strategy_a = 0
    curr_strategy_b = 0

    win_a = m * [0]
    loss_b = n * [0]
    curr_eps = math.inf
    k = 0

    lower_bounds = []
    upper_bounds = []

    while (curr_eps > eps):
        k += 1
        win_a = vector_addition(win_a, get_column_by_index(C, curr_strategy_b))
        loss_b = vector_addition(loss_b, get_row_by_index(C, curr_strategy_a))
        x[curr_strategy_a] += 1
        y[curr_strategy_b] += 1

        lower_bound = Fraction(min(loss_b), k)
        upper_bound = Fraction(max(win_a), k)
        lower_bounds.append(lower_bound)
        upper_bounds.append(upper_bound)

        curr_eps = min(upper_bounds) - max(lower_bounds)

        curr_strategy_a = get_rand_max_index(win_a)
        curr_strategy_b = get_rand_min_index(loss_b)

    average_cost = lower_bounds[-1] + upper_bounds[-1]
    average_cost /= 2

    x = [Fraction(i, k) for i in x]
    y = [Fraction(i, k) for i in y]

    return x, y, average_cost

def H(x, y):
    ''' The coefficients from example presented below
    a, b = Fraction(-3, 1), Fraction(3, 2)
    c = Fraction(18/5)
    d, e = Fraction(-18, 50), Fraction(-72, 25)
    '''
    a, b = Fraction(-5, 1), Fraction(5, 12)
    c = Fraction(10, 3)
    d, e = Fraction(-2, 3), Fraction(-4, 3)
    return a * x**2 + b * y**2 + c * x * y + d * x + e * y

def approximate_win_func_elem(H, i, j, N):
    return H(Fraction(i, N), Fraction(j, N))

def calc_expected_win(x, y, H):
    h = 0
    for i in range(len(H)):
        for j in range(len(H[0])):
            h += H[i][j] * x[i] * y[j]
    return h

def find_saddle_point(C):
    max_min = None
    min_max = None

    m = len(C)
    n = len(C[0])

    max_loss = []
    for i in range(n):
        max_loss.append(max(get_column_by_index(C, i)))
    y = get_min_index(max_loss)
    min_max = max_loss[y]

    min_win = []
    for i in range(n):
        min_win.append(min(get_row_by_index(C, i)))
    x = get_max_index(min_win)
    max_min = min_win[x]
    return max_min == min_max, x, y

def lattice_approximation_method(H, N):
    for n in range(1, N + 1):
        # create matrix for this iteration
        cur_H =[]
        for i in range(n + 1):
            cur_H.append([0] * (n + 1))
        # fill matrix with calculated values 
        for i in range(n + 1):
            for j in range(n + 1):
                cur_H[i][j] = approximate_win_func_elem(H, i, j, n)
        print("N = {:d}".format(n))
        for i in cur_H:
            print(*["{:10.3f}".format(float(j)) for j in i])
        has_saddle_point, x, y = find_saddle_point(cur_H)
        if has_saddle_point:
            print("Has saddle point: x = {:.3f}, y = {:.3f}, H = {:.3f}".format(float(x / n), float(y / n), float(cur_H[x][y])))
        else:
            print("Has no saddle point")
        eps = 0.01
        x_, y_, _ = brown_robinson_method(cur_H, eps)
        h = calc_expected_win(x_, y_, cur_H)
        print("Calculated with Brown-Robinson method with accuracy eps = {:.3f}, H = {:.3f}".format(eps, float(h)))
        print(h)

def main():
    lattice_approximation_method(H, 10)

if __name__ == "__main__":
    main()
