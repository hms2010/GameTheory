import math
import fractions
import random
from c import *
from sys import stdout

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


int_formatter = "{:^9d}"
float_formatter = "{:>4d}/{:<4d}"
str_formatter = "{:^9s}"
outline = "||"
separator = "|"
line_formatter = (outline + separator.join([int_formatter] * 3) 
+ outline + separator.join([int_formatter] * 3)
+ outline + separator.join([int_formatter] * 3)
+ outline + separator.join([float_formatter] * 3) + outline)

header_formatter = (outline + separator.join([str_formatter] * 3)
+ outline + "{:^29s}"
+ outline + "{:^29s}"
+ outline + separator.join([str_formatter] * 3) + outline)

def printHeader(curr_file):
    if curr_file:
        print(header_formatter.format("k", "A strat", "B strat", "Win A", "Loss B", "UpBound", "LowBound", "Eps"), file=curr_file)
        print(126 * "-", file=curr_file)

def printLine(curr_file, k, A, B, win_a, loss_b, upper_bound, lower_bound, eps):
    if curr_file:
        print(line_formatter.format(k, A, B, win_a[0], win_a[1], win_a[2], loss_b[0], loss_b[1], loss_b[2], upper_bound.numerator, upper_bound.denominator, lower_bound.numerator, lower_bound.denominator, eps.numerator, eps.denominator), file=curr_file)

out_file = stdout

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

    printHeader(out_file)

    while (curr_eps > eps):
        k += 1
        win_a = vector_addition(win_a, get_column_by_index(C, curr_strategy_b))
        loss_b = vector_addition(loss_b, get_row_by_index(C, curr_strategy_a))
        x[curr_strategy_a] += 1
        y[curr_strategy_b] += 1

        lower_bound = fractions.Fraction(min(loss_b), k)
        upper_bound = fractions.Fraction(max(win_a), k)
        lower_bounds.append(lower_bound)
        upper_bounds.append(upper_bound)

        curr_eps = min(upper_bounds) - max(lower_bounds)

        printLine(out_file, k, curr_strategy_a + 1, curr_strategy_b + 1, win_a, loss_b, upper_bound, lower_bound, curr_eps)

        curr_strategy_a = get_rand_max_index(win_a)
        curr_strategy_b = get_rand_min_index(loss_b)

    average_cost = lower_bounds[-1] + upper_bounds[-1]
    average_cost /= 2

    x = [fractions.Fraction(i, k) for i in x]
    y = [fractions.Fraction(i, k) for i in y]

    return x, y, average_cost

def main():
    eps = float(input("Enter eps: "))
    x, y, average_cost = brown_robinson_method(C, eps)
    print("x = (",*x, ")", file=out_file)
    print("y = (",*y, ")", file=out_file)
    print("x = (", *[float(i) for i in x], ")", file=out_file)
    print("y = (", *[float(i) for i in y], ")", file=out_file)
    print("Average cost is {} = {}".format(average_cost, float(average_cost)), file=out_file)

if __name__ == '__main__':
    main()
