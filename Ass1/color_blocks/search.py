from search_node import search_node
from color_blocks_state import color_blocks_state


def create_open_set():
    # OPEN list for A* search
    return []


def create_closed_set():
    # CLOSED list for explored nodes
    return []


def add_to_open(vn, open_set):
    open_set.append(vn)


def open_not_empty(open_set):
    return len(open_set) > 0


def get_best(open_set):
    # Find node with minimal f (breaking ties using __lt__)
    best_index = 0
    for i in range(1, len(open_set)):
        if open_set[i] < open_set[best_index]:
            best_index = i
    best_node = open_set[best_index]
    open_set.pop(best_index)   # remove from OPEN
    return best_node


def add_to_closed(vn, closed_set):
    closed_set.append(vn)


def duplicate_in_open(vn, open_set):
    """
    Returns True if a duplicate with better or equal g exists in OPEN.
    Returns False if:
      - no duplicate exists, OR
      - a duplicate exists but this path has lower g (in that case the old one is removed).
    """
    for i, node in enumerate(open_set):
        if node.state == vn.state:
            if vn.g < node.g:
                open_set.pop(i)
                return False  # new path is better
            else:
                return True   # existing path is better or equal
    return False  # no duplicate


def duplicate_in_closed(vn, closed_set):
    """
    Same logic as duplicate_in_open but for the CLOSED list.
    If a better path is found, remove the old node.
    """
    for i, node in enumerate(closed_set):
        if node.state == vn.state:
            if vn.g < node.g:
                closed_set.pop(i)
                return False
            else:
                return True
    return False


def print_path(path):
    # Helpful to print the result path
    for i in range(len(path)-1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.state_str)


def search(start_state, heuristic):
    """
    Standard A* search implementation.
    """
    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):

        current = get_best(open_set)

        # Goal test
        if color_blocks_state.is_goal_state(current.state):
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)

        # Expand neighbors
        for neighbor, cost in current.get_neighbors():
            new_node = search_node(neighbor, current.g + cost, heuristic(neighbor), current)

            # Skip if duplicate with better/equal path
            if not duplicate_in_open(new_node, open_set) and not duplicate_in_closed(new_node, closed_set):
                add_to_open(new_node, open_set)

    return None  # no solution
