from state import State
import argparse
import timeit
import itertools
from collections import deque
from heapq import heappush, heappop, heapify

BOARD_LEN = 0
BOARD_SIDE = 0

DESIRED_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]
INITIAL_STATE = list()

NODE_TARGETED = State
EXPANDED_NODES = 0
MAX_SEARCH_DEPTH = 0
MAX_FRONTIER_SIZE = 0
MOVES = list()
COSTS = set()
 

def ucs(start_state):

    global NODE_TARGETED, MAX_FRONTIER_SIZE,  MAX_SEARCH_DEPTH
    visited, queue = set(), deque([State(start_state, None, None, 0, 0, 0)])

    while queue:
        node = queue.popleft()
        visited.add(node.map)

        if node.state == DESIRED_STATE:
            NODE_TARGETED = node
            return queue
        near_nodes = expand(node)

        for near_node in near_nodes:
            if near_node.map not in visited:
                queue.append(near_node)
                visited.add(near_node.map)

                if near_node.depth > MAX_SEARCH_DEPTH:
                    MAX_SEARCH_DEPTH += 1

        if len(queue) > MAX_FRONTIER_SIZE:
            MAX_FRONTIER_SIZE = len(queue)


def ast(start_state):

    global MAX_FRONTIER_SIZE, NODE_TARGETED, MAX_SEARCH_DEPTH
    visited, heap, heap_entry, counter = set(), list(), {}, itertools.count()
    key = h(start_state)
    root = State(start_state, None, None, 0, 0, key)
    entry = (key, 0, root)
    heappush(heap, entry)
    heap_entry[root.map] = entry

    while heap:
        node = heappop(heap)
        visited.add(node[2].map)
        if node[2].state == DESIRED_STATE:
            NODE_TARGETED = node[2]
            return heap
        near_nodes = expand(node[2])
        for near_node in near_nodes:
            near_node.key = near_node.cost + h(near_node.state)
            entry = (near_node.key, near_node.move, near_node)
            if near_node.map not in visited:
                heappush(heap, entry)
                visited.add(near_node.map)
                heap_entry[near_node.map] = entry
                if near_node.depth > MAX_SEARCH_DEPTH:
                    MAX_SEARCH_DEPTH += 1
            elif near_node.map in heap_entry and near_node.key < heap_entry[near_node.map][2].key:
                hindex = heap.index((heap_entry[near_node.map][2].key,
                                     heap_entry[near_node.map][2].move,
                                     heap_entry[near_node.map][2]))
                heap[int(hindex)] = entry
                heap_entry[near_node.map] = entry
                heapify(heap)
        if len(heap) > MAX_FRONTIER_SIZE:
            MAX_FRONTIER_SIZE = len(heap)

def ida(start_state):

    global COSTS
    boundary = h(start_state)
    while 1:
        response = dls(start_state, boundary)
        if type(response) is list:
            return response
            break
        boundary = response
        COSTS = set()

def dls(start_state, boundary):

    global MAX_FRONTIER_SIZE, NODE_TARGETED, MAX_SEARCH_DEPTH, COSTS
    visited, stack = set(), list([State(start_state, None, None, 0, 0, boundary)])
    while stack:
        node = stack.pop()
        visited.add(node.map)
        if node.state == DESIRED_STATE:
            NODE_TARGETED = node
            return stack
        if node.key > boundary:
            COSTS.add(node.key)
        if node.depth < boundary:
            near_nodes = reversed(expand(node))
            for near_node in near_nodes:
                if near_node.map not in visited:
                    near_node.key = near_node.cost + h(near_node.state)
                    stack.append(near_node)
                    visited.add(near_node.map)
                    if near_node.depth > MAX_SEARCH_DEPTH:
                        MAX_SEARCH_DEPTH += 1
            if len(stack) > MAX_FRONTIER_SIZE:
                MAX_FRONTIER_SIZE = len(stack)
    return min(COSTS)


def expand(node):
    
    global EXPANDED_NODES
    EXPANDED_NODES += 1

    near_nodes = list()

    near_nodes.append(State(move(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    near_nodes.append(State(move(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    near_nodes.append(State(move(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    near_nodes.append(State(move(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))

    nodes = [near_node for near_node in near_nodes if near_node.state]

    return nodes


def move(state, position):

    new_state = state[:]
    index = new_state.index(0)

    if position == 1:  # Cima

        if index not in range(0, BOARD_SIDE):

            temp = new_state[index - BOARD_SIDE]
            new_state[index - BOARD_SIDE] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None
            
    if position == 2:  # Baixo

        if index not in range(BOARD_LEN - BOARD_SIDE, BOARD_LEN):

            temp = new_state[index + BOARD_SIDE]
            new_state[index + BOARD_SIDE] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 3:  # Esquerda

        if index not in range(0, BOARD_LEN, BOARD_SIDE):

            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 4:  # Direita

        if index not in range(BOARD_SIDE - 1, BOARD_LEN, BOARD_SIDE):

            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None


def h(state):

    return sum(abs(b % BOARD_SIDE - g % BOARD_SIDE) + abs(b//BOARD_SIDE - g//BOARD_SIDE)
               for b, g in ((state.index(i), DESIRED_STATE.index(i)) for i in range(1, BOARD_LEN)))


def moves_tracker():

    current_node = NODE_TARGETED
    while INITIAL_STATE != current_node.state:

        if current_node.move == 1:
            movement = 'cima'
        elif current_node.move == 2:
            movement = 'baixo'
        elif current_node.move == 3:
            movement = 'esquerda'
        else:
            movement = 'direita'

        MOVES.insert(0, movement)
        current_node = current_node.parent
        
    return MOVES


def export(frontier, time):

    global MOVES
    MOVES = moves_tracker()

    file = open('resolucao.txt', 'w')
    file.write("Movimentos: " + str(MOVES))
    file.write("\nCusto da solucao: " + str(len(MOVES)))
    file.write("\nNodos expandidos: " + str(EXPANDED_NODES))
    file.write("\nTamanho da fronteira: " + str(len(frontier)))
    file.write("\nTamanho maximo da fronteira: " + str(MAX_FRONTIER_SIZE))
    file.write("\nProfundidade da busca: " + str(NODE_TARGETED.depth))
    file.write("\nProfundidade maxima da busca: " + str(MAX_SEARCH_DEPTH))
    file.write("\nTempo gasto em ms: " + format(time, '.8f'))
    file.close()


def read(configuration):

    global BOARD_LEN, BOARD_SIDE

    data = configuration.split(",")

    for element in data:
        INITIAL_STATE.append(int(element))

    BOARD_LEN = len(INITIAL_STATE)
    BOARD_SIDE = int(BOARD_LEN ** 0.5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('algorithms')
    parser.add_argument('inicio')
    args = parser.parse_args()
    read(args.inicio)
    function = functions_map[args.algorithms]
    start = timeit.default_timer()
    stop = timeit.default_timer()
    frontier = function(INITIAL_STATE)
    export(frontier, stop-start)


functions_map = {
    'ucs': ucs,
    'ast': ast,
    'ida': ida
}