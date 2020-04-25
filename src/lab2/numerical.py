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

    cost = max(lower_bounds) + Fraction(curr_eps, 2)

    x = [Fraction(i, k) for i in x]
    y = [Fraction(i, k) for i in y]

    return x, y, cost

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

def limit(a, eps):
    ff = False
    N = -1
    for i in range(1, len(a)):
        if abs(a[i] - a[i - 1]) < eps:
            N = i
            ff = True
        elif ff:
            N = -1
            ff = False
    if not ff:
        return math.inf
    return a[N] 


def calc_grid_element(H, i, j, N):
    return H(Fraction(i, N), Fraction(j, N))

def generate_grid_approximation(H, n):
    cur_H = []
    for i in range(n + 1):
        cur_H.append([0] * (n + 1))
    # fill matrix with calculated values 
    for i in range(n + 1):
        for j in range(n + 1):
            cur_H[i][j] = calc_grid_element(H, i, j, n)
    return cur_H

def grid_approximation_method(H, eps):
    cost_array = []
    n = 1
    while(True):
        # create matrix for this iteration
        cur_H = generate_grid_approximation(H, n)
        print("N = {:d}".format(n))
        for i in cur_H:
            print(*["{:8.3f}".format(float(j)) for j in i])
        has_saddle_point, x, y = find_saddle_point(cur_H)
        if has_saddle_point:
            h = cur_H[x][y]
            x = Fraction(x, n)
            y = Fraction(y, n)
            print("Has saddle point: x = {:}, y = {:}, h = {:} = {:.3f}".format(x, y, h, float(h)))
        else:
            print("Has no saddle point")
            x, y, h = brown_robinson_method(cur_H, eps)
            x = Fraction(get_max_index(x), n)
            y = Fraction(get_max_index(y), n)
            print("Calculated with Brown-Robinson method with accuracy eps = {:.3f} solution: x = {:}, y = {:}, h = {:} = {:.3f}".format(eps, x, y, h, float(h)))
        cost_array.append(h)
        lim = limit(cost_array, eps)
        if lim != math.inf:
            return x, y, lim
        n += 1

def main():
    x, y, c = grid_approximation_method(H, 0.001)
    print("Found solution is: x = {:}, y = {:}, c = {:} = {:.3f}".format(x, y, c, float(c)))

if __name__ == "__main__":
    main()
