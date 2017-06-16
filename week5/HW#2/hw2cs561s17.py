import sys
import copy


class Node(object):
    adj_dict = {}
    player1_color_score = {}
    player2_color_score = {}

    def __init__(self, level, states_list, colors_list):
        self.player1_states = []
        self.player2_states = []
        self.level = level
        self.state_colored_dict = {}
        self.state_none_colored_dict = {}
        for state in states_list:
            self.state_none_colored_dict[state] = set(colors_list)

    def expand(self, player):
        """Generate a queue of next nodes, all are checked by the ac3
        to make sure the validity."""
        neibor_state_set = set()
        for state in self.state_colored_dict:
            for adj_state in Node.adj_dict[state]:
                if adj_state not in self.state_colored_dict:

                    neibor_state_set.add(adj_state)

        next_nodes_list = []
        for state in sorted(list(neibor_state_set)):
            for color in sorted(self.state_none_colored_dict[state]):
                next_node = copy.copy(self)
                next_node.state_none_colored_dict = {}
                next_node.state_colored_dict = {}
                flag = False
                for key in self.state_colored_dict:
                    next_node.state_colored_dict[key] = str(self.state_colored_dict[key])
                    if self.state_colored_dict[key] == color and state in Node.adj_dict[key]:
                        flag = True
                        break
                if flag:
                    continue
                next_node.player1_states = list(self.player1_states)
                next_node.player2_states = list(self.player2_states)

                for key in self.state_none_colored_dict:
                    next_node.state_none_colored_dict[key] = set(self.state_none_colored_dict[key])

                next_node.set_color(player, (state, color))
                next_node.level += 1
                next_node.reduce_none_set(state)
                next_nodes_list.append(next_node)

        return next_nodes_list

    def reduce_none_set(self, modified_state):
        # delete possible colors in none set
        for end in Node.adj_dict[modified_state]:
            if end in self.state_none_colored_dict:
                color = self.state_colored_dict[modified_state]
                if color in self.state_none_colored_dict[end]:
                    self.state_none_colored_dict[end].remove(color)

    def set_color(self, player, action):
        """Update the node by the action, (state, color). If the node
        is valid after ac3, then we return true, else return false"""
        state, color = action
        del self.state_none_colored_dict[state]
        self.state_colored_dict[state] = color
        if player == 1:
            self.player1_states.append(state)
        else:
            self.player2_states.append(state)

    def get_eval(self):
        """Calculate the utility value"""
        score = sum([Node.player1_color_score[self.state_colored_dict[t]] for t in self.player1_states])
        score -= sum([Node.player2_color_score[self.state_colored_dict[t]] for t in self.player2_states])
        return score


# minmax with alpha-beta pruning implementation
log = []


class NextNodes:

    def __init__(self, node, player):
        self.player = player
        self.i = 0
        self.node = node
        next_node_set = set()
        next_node_none_set = set()
        for state in node.state_colored_dict:
            for adj_state in Node.adj_dict[state]:
                if adj_state not in node.state_colored_dict:
                    for color in node.state_none_colored_dict[adj_state]:
                        if color != node.state_colored_dict[state]:
                            next_node_set.add((adj_state, color))
                        else:
                            next_node_none_set.add((adj_state, color))
        self.next_node_list = sorted(list(next_node_set.difference(next_node_none_set)))

    def __iter__(self):
        return self

    def next(self):
        if not self.next_node_list or self.i >= len(self.next_node_list):
            return None

        action = self.next_node_list[self.i]
        self.i += 1
        next_node = copy.copy(self.node)
        next_node.state_none_colored_dict = {}
        next_node.state_colored_dict = {}
        for key in self.node.state_colored_dict:
            next_node.state_colored_dict[key] = str(self.node.state_colored_dict[key])
        next_node.player1_states = list(self.node.player1_states)
        next_node.player2_states = list(self.node.player2_states)

        for key in self.node.state_none_colored_dict:
            next_node.state_none_colored_dict[key] = set(self.node.state_none_colored_dict[key])

        next_node.set_color(self.player, action)
        next_node.level += 1
        next_node.reduce_none_set(state)
        return next_node


def alpha_beta_search(node, max_level):
    """Search the path to ge the max value"""
    return max_value(node, -float('inf'), float('inf'), max_level)


def max_value(node, alpha, beta, max_level):
    """Select the next step to maximize the value,
    return the path and value"""
    next_node_it = NextNodes(node, 1)
    # next_nodes_list = node.expand(1)

    value = -float('inf')
    if node.level == max_level or not next_node_it.next_node_list:
        value = node.get_eval()

    path = None
    log.append(node.player2_states[-1]
               + ', '
               + node.state_colored_dict[node.player2_states[-1]]
               + ', '
               + str(node.level)
               + ', '
               + str(value)
               + ', '
               + str(alpha)
               + ', '
               + str(beta)
               )
    # print log[-1]

    if node.level == max_level or not next_node_it.next_node_list:
        return node.get_eval(), []

    next_node = next_node_it.next()
    while next_node:
        next_value, next_path = min_value(next_node, alpha, beta, max_level)

        if next_value > value:
            value = next_value
            path = next_path
            path.insert(0, (next_node.player1_states[-1], next_node.state_colored_dict[next_node.player1_states[-1]]))

        if value >= beta:
            log.append(node.player2_states[-1]
                       + ', '
                       + node.state_colored_dict[node.player2_states[-1]]
                       + ', '
                       + str(node.level)
                       + ', '
                       + str(value)
                       + ', '
                       + str(alpha)
                       + ', '
                       + str(beta)
                       )
            # print log[-1]
            return value, path
        alpha = max(alpha, value)
        log.append(node.player2_states[-1]
                   + ', '
                   + node.state_colored_dict[node.player2_states[-1]]
                   + ', '
                   + str(node.level)
                   + ', '
                   + str(value)
                   + ', '
                   + str(alpha)
                   + ', '
                   + str(beta)
                   )
        next_node = next_node_it.next()
        # print log[-1]
    return value, path


def min_value(node, alpha, beta, max_level):
    """Select the next step to minimize the value,
    return the path and value"""
    # next_nodes_list = node.expand(2)
    next_node_it = NextNodes(node, 2)

    value = +float('inf')
    if node.level == max_level or not next_node_it.next_node_list:
        value = node.get_eval()

    path = None

    log.append(node.player1_states[-1]
               + ', '
               + node.state_colored_dict[node.player1_states[-1]]
               + ', '
               + str(node.level)
               + ', '
               + str(value)
               + ', '
               + str(alpha)
               + ', '
               + str(beta)
               )
    # print log[-1]

    if node.level == max_level or not next_node_it.next_node_list:
        return node.get_eval(), []

    next_node = next_node_it.next()
    while next_node:
        next_value, next_path = max_value(next_node, alpha, beta, max_level)

        if next_value < value:
            value = min(value, next_value)
            path = next_path
            path.insert(0, (next_node.player2_states[-1], next_node.state_colored_dict[next_node.player2_states[-1]]))

        if value <= alpha:
            log.append(node.player1_states[-1]
                       + ', '
                       + node.state_colored_dict[node.player1_states[-1]]
                       + ', '
                       + str(node.level)
                       + ', '
                       + str(value)
                       + ', '
                       + str(alpha)
                       + ', '
                       + str(beta)
                       )
            # print log[-1]
            return value, path

        beta = min(beta, value)
        log.append(node.player1_states[-1]
                   + ', '
                   + node.state_colored_dict[node.player1_states[-1]]
                   + ', '
                   + str(node.level)
                   + ', '
                   + str(value)
                   + ', '
                   + str(alpha)
                   + ', '
                   + str(beta)
                   )
        next_node = next_node_it.next()
        # print log[-1]
    return value, path


if __name__ == '__main__':
    log = []
    file_name = sys.argv[2]
    with open(file_name, 'r') as f:
        lines = f.read().splitlines()

    color_list = lines[0].split(', ')

    pre_set_color = []  # (state, color, player)
    for seg in lines[1].split(', '):
        data = seg.split(': ')
        state = data[0]
        data_2 = data[1].split('-')
        color = data_2[0]
        player = int(data_2[1])
        pre_set_color.append((state, color, player))

    max_level = int(lines[2])

    player1_score_dict = {}
    for seg in lines[3].split(', '):
        data = seg.split(': ')
        player1_score_dict[data[0]] = int(data[1])

    player2_score_dict = {}
    for seg in lines[4].split(', '):
        data = seg.split(': ')
        player2_score_dict[data[0]] = int(data[1])

    state_set = set()
    adj_dict = {}
    for line in lines[5:]:
        data = line.split(': ')
        state = data[0]
        state_set.add(state)
        adj_list = []
        for adj in data[1].split(', '):
            adj_list.append(adj.strip())
        adj_dict[state] = adj_list

    node = Node(0, list(state_set), color_list)
    Node.player1_color_score = player1_score_dict
    Node.player2_color_score = player2_score_dict
    Node.adj_dict = adj_dict

    for state, color, player in pre_set_color:
        node.set_color(player, (state, color))
    value, path = alpha_beta_search(node, max_level)
    with open('output.txt', 'w') as f:
        for line in log:
            f.write(line+'\n')
        f.write(path[0][0] + ', ' + path[0][1] + ', ' + str(value))


