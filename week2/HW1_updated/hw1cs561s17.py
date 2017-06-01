import re
from collections import deque
from heapq import heappop, heappush, heapify
import sys


# define the graph node
class Node(object):
    def __init__(self, x):
        self.val = x
        self.adjacent_list = []
        self.adjacent_cost = []
        self.is_visited = False
        self.parent = self

    def __cmp__(self, other):
        '''
        This used to make sure we call it in alphabet order when using heapq in UCS
        '''
        if self.val == other.val:
            return 0
        elif self.val > other.val:
            return 1
        else:
            return -1


# build the path by find its parent recursively
def build_path(node):
    path = []
    while node.parent != node:
        path.insert(0, node.val)
        node = node.parent
    path.insert(0, node.val)
    return path


# UCS search for the d
def ucs(s_node, d_val, fuel):
    # init the priority queue
    s_node.is_visited = True
    h = []
    heappush(h, (0, s_node))

    # loop until the stack is empty
    while len(h) > 0:

        # deque one node to process
        cost, node = heappop(h)
        node.is_visited = True

        # check if we meet the goal
        if node.val == d_val:
            path = build_path(node)
            return path, fuel - cost

        # update the queue in alphabet order
        for next_node, cost_edge in zip(node.adjacent_list, node.adjacent_cost):

            # only put nodes to the queue when fuel is enough
            if cost_edge <= fuel - cost and not next_node.is_visited:

                # a path to the node has already been found waiting to be expand, we have to check whether update it
                if next_node in map(lambda t: t[1], h):
                    idx = map(lambda t: t[1], h).index(next_node)
                    if cost + cost_edge < h[idx][0]:
                        h[idx] = h[-1]      # if need update, we delete it
                        heapify(h)
                    else:
                        continue
                # python will compare tuple from the first pos, if it is the same then the next pos.
                # this makes sure we will process the node in alphabet order when their cost are the same
                next_node.parent = node
                heappush(h, (cost + cost_edge, next_node))

    return None


# DFS search for the d
def dfs(s_node, d_val, fuel):
    # init the stack for dfs
    s_node.is_visited = True
    stack = [(s_node, fuel)]

    # loop until the stack is empty
    while len(stack) > 0:

        # deque one node to process
        node, fuel_left = stack.pop()
        node.is_visited = True

        # check if we meet the goal
        if node.val == d_val:
            path = build_path(node)
            return path, fuel_left

        # update the queue
        for next_node, cost in sorted(zip(node.adjacent_list, node.adjacent_cost), key=lambda t: t[0].val, reverse=True):
            # only put nodes to the queue when fuel is enough
            if cost <= fuel_left and not next_node.is_visited:
                next_node.parent = node
                stack.append((next_node, fuel_left - cost))

    return None


# BFS search for the d
def bfs(s_node, d_val, fuel):
    # init the queue for bfs
    s_node.is_visited = True
    queue = deque([(s_node, fuel)])

    # loop until the queue is empty
    while len(queue) > 0:

        # deque one node to process
        node, fuel_left = queue.popleft()
        node.is_visited = True

        # check if we meet the goal
        if node.val == d_val:
            path = build_path(node)
            return path, fuel_left

        # update the queue
        for next_node, cost in sorted(zip(node.adjacent_list, node.adjacent_cost), key=lambda t: t[0].val):

            # only put nodes to the queue when fuel is enough
            if cost <= fuel_left and not next_node.is_visited:
                next_node.parent = node
                queue.append((next_node, fuel_left - cost))

    return None

if __name__ == '__main__':
    file_name = sys.argv[2]  # get file name from parameters

    # read in the file and extract info
    with open(file_name, 'r') as f:
        search_type = f.readline().replace('\n', '')        # get the search type: DFS, BFS, UCS
        fuel = int(f.readline().replace('\n', ''))          # get fuel
        start_node_val = f.readline().replace('\n', '')     # start point
        end_node_val = f.readline().replace('\n', '')       # end point

        # split the edge info
        edge_match = re.compile('[\S^:\-]+-\d+')
        edge_split = re.compile('([\S^:\-]+)(?:-)(\d+)')

        # construct start point and end point
        start_node = Node(start_node_val)
        end_node = Node(end_node_val)

        # build  the set for node
        node_set = {start_node_val: start_node, end_node_val: end_node}

        for line in f:
            # read in the value of the node
            node_val = re.compile('((\S)+)(?::.)').search(line).group(1)

            # get the node from node name
            if node_val not in node_set:
                node_set[node_val] = Node(node_val)
            node = node_set[node_val]

            # process each edge to build the graph
            edge_list = re.findall(edge_match, line)
            for edge in edge_list:
                re_result = re.search(edge_split, edge)     # extract edge name and cost
                edge_node_val = re_result.group(1)
                edge_cost = int(re_result.group(2))

                # get node from name
                if edge_node_val not in node_set:
                    node_set[edge_node_val] = Node(edge_node_val)
                edge_node = node_set[edge_node_val]

                # append to the list
                node.adjacent_list.append(edge_node)
                node.adjacent_cost.append(edge_cost)

    # select the search type
    if search_type == 'DFS':
        result = dfs(start_node, end_node_val, fuel)
    elif search_type == 'BFS':
        result = bfs(start_node, end_node_val, fuel)
    else:
        result = ucs(start_node, end_node_val, fuel)

    # check the result if we find the path
    if result:
        path, fuel = result

        # generate the output string
        path_string = ''
        for w in path[:-1]:
            path_string += w
            path_string += '-'
        path_string += path[-1]
        output = path_string + ' ' + str(fuel)
    else:
        output = 'No Path'

    # write output to the file
    with open('output.txt', 'w') as f:
        f.write(output)
