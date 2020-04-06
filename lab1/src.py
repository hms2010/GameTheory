import math
import fractions
import random
from c import C

def randMaxIndex(arr):
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

def randMinIndex(arr):
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

def getRowByIndex(matrix, index):
    return matrix[index]

def getColumnByIndex(matrix, index):
    return [matrix[i][index] for i in range(len(matrix))]

def getMaxIndex(arr):
    return arr.index(max(arr))

def getMinIndex(arr):
    return arr.index(min(arr))

def vectorAdd(a, b):
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

def printHeader():
    print(header_formatter.format("k", "A strat", "B strat", "Win A", "Loss B", "UpBound", "LowBound", "Eps"))
    print(126 * "-")

def printLine(k, A, B, win_A, loss_B, upper_bound, lower_bound, eps):
    print(line_formatter.format(k, A, B, win_A[0], win_A[1], win_A[2], loss_B[0], loss_B[1], loss_B[2], upper_bound.numerator, upper_bound.denominator, lower_bound.numerator, lower_bound.denominator, eps.numerator, eps.denominator))

def main():
    random.seed()

    eps = float(input("Enter eps: "))

    n = len(C) # number of player A strategies; number of rows in C
    m = len(C[0])      # number of player B strategies; number of columns in C

    printHeader()

    upper_bounds = []
    lower_bounds = []

    currEps = math.inf
    currIter = 0
    currStrategy_A = 0
    currStrategy_B = 0
    win_A = [0] * n
    loss_B = [0] * m

    x = [0] * n
    y = [0] * m
    while (currEps > eps):
        currIter += 1
        x[currStrategy_A] += 1
        y[currStrategy_B] += 1

        win_A = vectorAdd(win_A, getColumnByIndex(C, currStrategy_A))
        loss_B = vectorAdd(loss_B, getRowByIndex(C, currStrategy_B))

        upper_bound = fractions.Fraction(max(win_A), currIter)
        upper_bounds.append(upper_bound)

        lower_bound = fractions.Fraction(min(loss_B), currIter)
        lower_bounds.append(lower_bound)

        currEps = min(upper_bounds) - max(lower_bounds)

        printLine(currIter, currStrategy_A + 1, currStrategy_B + 1, win_A, loss_B, upper_bound, lower_bound, currEps)

        currStrategy_A, currStrategy_B = randMinIndex(loss_B), randMaxIndex(win_A)

    average_cost = lower_bounds[-1] + upper_bounds[-1]
    average_cost /= 2
    print("Average cost is {} = {}".format(average_cost, float(average_cost)))

    x = [fractions.Fraction(i, currIter) for i in x]
    y = [fractions.Fraction(i, currIter) for i in y]
    print("x = (",*x, ")")
    print("y = (",*y, ")")
    print ("x = (", *[float(i) for i in x], ")")
    print ("y = (", *[float(i) for i in y], ")")

if __name__ == "__main__":
    main()