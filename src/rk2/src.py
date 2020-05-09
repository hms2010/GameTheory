import random
import math

g_cur_game = {
    'tree_height': 5,
    'players_num': 3,
    'strats_num': [2, 3, 2],
    'min_cost': -50,
    'max_cost': 50
}

class Edge:
    tag = None
    parent = None
    cost_array = []
    children = []
    path_last = None
    def __init__(self, _parent, _tag):
        self.parent = _parent
        self.tag = _tag
    def __repr__(self):
        out = "{}".format(self.tag)
        if self.parent:
            out = "{}({})".format(out, self.parent.tag)
        if self.cost_array:
            return "{}/{}\\".format(out, self.cost_array)
        return out

def generate_random_game_tree(cur_game):
    random.seed()
    edges = []
    cnt = 0
    for i in range(cur_game['tree_height']):
        if i == 0: # game just begins; add root
            edges.append([Edge(None, cnt)])
            cnt += 1
            continue
        cur_level = []
        prev_level = edges[i - 1]
        not_leaves = []
        not_leaves_len = random.choice(range(1, len(prev_level) + 1))
        for k in range(not_leaves_len):
            elem = random.choice(range(0, len(prev_level)))
            if elem not in not_leaves:
                not_leaves.append(elem)
        not_leaves.sort()
        for k in range(len(prev_level)):
            if k in not_leaves:
                children = []
                for _ in range(cur_game['strats_num'][(i - 1) % cur_game['players_num']]):
                    cur_edge = Edge(prev_level[k], cnt)
                    children.append(cur_edge)
                    cur_level.append(cur_edge)
                    cnt += 1
                prev_level[k].children = children
            else:
                prev_level[k].cost_array = random.choices(range(cur_game['min_cost'], cur_game['max_cost'] + 1), k = cur_game['players_num'])
                prev_level[k].path_last = prev_level[k]
        edges.append(cur_level)
    for cur_edge in edges[-1]:
        cur_edge.cost_array = random.choices(range(cur_game['min_cost'], cur_game['max_cost'] + 1), k = cur_game['players_num'])
        cur_edge.path_last = cur_edge
    return edges

def print_tree_by_level(tree):
    for level in tree:
        print(level)

def get_path(edge):
    path = []
    while edge.parent:
        path.append(edge.tag)
        edge = edge.parent
    path.append(edge.tag)
    return path[::-1]

def reverse_induction(tree, cur_game):
    print("Game strategies tree:")
    print_tree_by_level(tree)

    for i in range(1, len(tree)):
        parent_level = cur_game['tree_height'] - 1 - i
        for k in range(len(tree[parent_level])):
            parent = tree[parent_level][k]
            if parent.children:
                cur_max_strat = -math.inf
                for cur_edge_ind in range(len(parent.children)):
                    cur_edge = parent.children[cur_edge_ind]
                    if cur_edge.cost_array[parent_level % cur_game['players_num']] > cur_max_strat:
                        cur_max_strat = cur_edge.cost_array[parent_level % cur_game['players_num']]
                        cur_player_strat = cur_edge_ind
                parent.cost_array = parent.children[cur_player_strat].cost_array
                parent.path_last = parent.children[cur_player_strat].path_last
        print("After {} step:".format(i))
        print_tree_by_level(tree)
    return tree[0][0]

def get_max_index(arr):
    return arr.index(max(arr))

tree = generate_random_game_tree(g_cur_game)
solution = reverse_induction(tree, g_cur_game)
path = get_path(solution.path_last)
print("Game cost array: {}".format(solution.cost_array))
print("Winner is {} player ({})".format(1 + get_max_index(solution.cost_array), max(solution.cost_array)))
print("Path is {}".format(path))