import random

MAX_COST = 50
MIN_COST = -MAX_COST

def generate_game(nrows, ncols):
    random.seed()
    G = []
    for i in range(nrows):
        G.append([0] * ncols)
        for j in range(ncols):
            G[i][j] = {'a': random.randint(MIN_COST, MAX_COST), 'b': random.randint(MIN_COST, MAX_COST)}
    return G

def print_game_matrix(G):
    for i in G:
        line = ""
        for j in i:
            cur_elem = "{:6.2f}/{:6.2f}".format(j['a'], j['b'])
            if not line:
                line = cur_elem
            else:
                line = ", ".join([line, cur_elem])
        print(line)

class player_strategy:
    strat = None
    cost = None
    def __init__(self, _strat, _cost):
        self.strat = _strat
        self.cost = _cost

    def __eq__(self, other):
        return isinstance(other, player_strategy) and self.strat == other.strat and self.cost == other.cost

def print_point(full_point):
    # full_point = {'a': player_strategy(i, G[i][j]['a']), 'b': player_strategy(j, G[i][j]['b'])}
    print("G[{:d}][{:d}] = ({:6.2f}/{:6.2f})".format(full_point['a'].strat + 1, full_point['b'].strat + 1, full_point['a'].cost, full_point['b'].cost))

def check_nash_equilibrium(point, G):
    na = len(G)
    nb = len(G[0])
    is_nash_equilibrium = True
    # point = {'a': player_strategy(i, G[i][j]['a']), 'b': player_strategy(j, G[i][j]['b'])}
    fixed_strat = point['a'].strat
    for b_strat in range(nb):
        if point['b'].strat == b_strat:
            continue
        if point['b'].cost < G[fixed_strat][b_strat]['b']:
            is_nash_equilibrium = False

    fixed_strat = point['b'].strat
    for a_strat in range(na):
        if point['a'].strat == a_strat:
            continue
        if point['a'].cost < G[a_strat][fixed_strat]['a']:
            is_nash_equilibrium = False
    return is_nash_equilibrium

def get_nash_equilibrium_strats(G):
    points = []
    # point = {'a': player_strategy(i, G[i][j]['a']), 'b': player_strategy(j, G[i][j]['b'])}
    na = len(G)
    nb = len(G[0])
    for i in range(na):
        for j in range(nb):
            point = {'a': player_strategy(i, G[i][j]['a']), 'b': player_strategy(j, G[i][j]['b'])}
            if check_nash_equilibrium(point, G):
                if point not in points:
                    points.append(point)
    return points

def check_pareto_efficiency(point, G):
    na = len(G)
    nb = len(G[0])
    # point = {'a': player_strategy(i, G[i][j]['a']), 'b': player_strategy(j, G[i][j]['b'])}
    x = point['a'].strat
    y = point['b'].strat

    for a_strat in range(na):
        for b_strat in range(nb):
            if(G[a_strat][b_strat]['a'] >= G[x][y]['a'] and G[a_strat][b_strat]['b'] >= G[x][y]['b']):
                if G[a_strat][b_strat]['a'] > G[x][y]['a'] or G[a_strat][b_strat]['b'] >  G[x][y]['b']:
                    return False
    return True

def get_pareto_efficiency_strats(G):
    points = []
    # point = {'a': player_strategy(i, G[i][j]['a']), 'b': player_strategy(j, G[i][j]['b'])}
    na = len(G)
    nb = len(G[0])
    for i in range(na):
        for j in range(nb):
            point = {'a': player_strategy(i, G[i][j]['a']), 'b': player_strategy(j, G[i][j]['b'])}
            if check_pareto_efficiency(point, G):
                if point not in points:
                    points.append(point)
    return points

def get_common_elems(a, b):
    common_elems = []
    if len(a) > len(b):
        for i in range(len(b)):
            if b[i] in a:
                common_elems.append(b[i])
    else:
        for i in range(len(a)):
            if a[i] in b:
                common_elems.append(a[i])
    return common_elems

def fam_bet_game():
    G = [
            [{'a': 4, 'b': 1}, {'a': 0, 'b': 0}],
            [{'a': 0, 'b': 0}, {'a': 1, 'b': 4}]
        ]
    print("Family bet game:")
    print_game_matrix(G)
    nash_eq_points = get_nash_equilibrium_strats(G)
    pareto_opt_points = get_pareto_efficiency_strats(G)
    both = get_common_elems(nash_eq_points, pareto_opt_points)

    print("Nash equilibrium points:")
    for i in nash_eq_points:
       print_point(i)
    print("Pareto optimal points:")
    for i in pareto_opt_points:
        print_point(i)
    print("Both criterias:")
    for i in both:
        print_point(i)

def prisoners_dilemma_game():
    G = [
            [{'a': -5, 'b': -5}, {'a': 0, 'b': -10}],
            [{'a': -10, 'b': 0}, {'a': -1, 'b': -1}]
        ]
    print("Prisoner's dilemma game:")
    print_game_matrix(G)
    nash_eq_points = get_nash_equilibrium_strats(G)
    pareto_opt_points = get_pareto_efficiency_strats(G)
    both = get_common_elems(nash_eq_points, pareto_opt_points)

    print("Nash equilibrium points:")
    for i in nash_eq_points:
       print_point(i)
    print("Pareto optimal points:")
    for i in pareto_opt_points:
        print_point(i)
    print("Both criterias:")
    for i in both:
        print_point(i)

def crossroads_game():
    random.seed()
    eps = random.randint(1, 100) / 100
    G = [
            [{'a': 1, 'b': 1}, {'a': 1 - eps, 'b': 2}],
            [{'a': 2, 'b': 1 - eps}, {'a': 0, 'b': 0}]
        ]
    print("Crossroads game:")
    print_game_matrix(G)
    nash_eq_points = get_nash_equilibrium_strats(G)
    pareto_opt_points = get_pareto_efficiency_strats(G)
    both = get_common_elems(nash_eq_points, pareto_opt_points)

    print("Nash equilibrium points:")
    for i in nash_eq_points:
       print_point(i)
    print("Pareto optimal points:")
    for i in pareto_opt_points:
        print_point(i)
    print("Both criterias:")
    for i in both:
        print_point(i)

def main():
    fam_bet_game()
    print()
    prisoners_dilemma_game()
    print()
    crossroads_game()
    print()
    try:
        from game_data import G
        print("Game was imported")
    except ModuleNotFoundError:
        n = 10 # int(input("n = "))
        m = 10 # int(input("m = "))
        G = generate_game(n, m)
        with open("game_data.py", 'w') as fout:
            fout.write('G = {:}'.format(G))
            fout.close()
        print("Game was created")

    print("Game n x m:")
    print_game_matrix(G)
    nash_eq_points = get_nash_equilibrium_strats(G)
    print("Nash equilibrium points:")
    for i in nash_eq_points:
       print_point(i)
    pareto_opt_points = get_pareto_efficiency_strats(G)
    print("Pareto optimal points:")
    for i in pareto_opt_points:
        print_point(i)
    print("Both criterias:")
    both = get_common_elems(nash_eq_points, pareto_opt_points)
    for i in both:
        print_point(i)

if __name__ == '__main__':
    main()