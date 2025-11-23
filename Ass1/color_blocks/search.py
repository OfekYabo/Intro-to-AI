import heapq
from search_node import search_node
from color_blocks_state import color_blocks_state


def create_open_set():
    """
    OPEN is represented as a pair:
      - open_heap: min-heap of search_node (ordered by f, then h via __lt__)
      - open_dict: dict mapping state -> search_node (best g in OPEN)
    """
    open_heap = []
    open_dict = {}
    return open_heap, open_dict


def create_closed_set():
    # CLOSED as a dict: state -> search_node
    return {}


def add_to_open(vn, open_set):
    open_heap, open_dict = open_set
    heapq.heappush(open_heap, vn)
    open_dict[vn.state] = vn


def open_not_empty(open_set):
    open_heap, _ = open_set
    return len(open_heap) > 0


def get_best(open_set):
    """
    Pop the best node (lowest f) from the heap.
    Skip stale entries that are no longer the current best version in open_dict.
    """
    open_heap, open_dict = open_set

    while open_heap:
        best_node = heapq.heappop(open_heap)
        current = open_dict.get(best_node.state)
        if current is best_node:
            # This is the current best version; remove from dict and return
            del open_dict[best_node.state]
            return best_node
        # else: stale entry (an older, worse node for this state), skip it

    return None  # should not happen if OPEN is used correctly


def add_to_closed(vn, closed_set):
    closed_set[vn.state] = vn


def duplicate_in_open(vn, open_set):
    _, open_dict = open_set
    existing = open_dict.get(vn.state)
    if existing is None:
        return False
    if existing.g <= vn.g:
        return True
    open_dict[vn.state] = vn
    return False


def duplicate_in_closed(vn, closed_set):
    existing = closed_set.get(vn.state)
    if existing is None:
        return False

    if existing.g <= vn.g:
        return True  # existing path is better or equal
    else:
        # better path found; reopen by removing old
        del closed_set[vn.state]
        return False


def print_path(path):
    # Helpful to print the result path
    for i in range(len(path) - 1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.get_state_str)


def search(start_state, heuristic):
    """
    Standard A* search implementation using:
      - OPEN: (heap, dict)
      - CLOSED: dict
    """
    open_set = create_open_set()
    closed_set = create_closed_set()

    # Create start node without h, then compute h once and cache it
    start_node = search_node(start_state, 0, h=None)
    start_node.h = heuristic(start_state)
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):

        current = get_best(open_set)
        if current is None:
            break  # safety

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
            new_g = current.g + cost
            # Create node without computing h yet
            new_node = search_node(neighbor, new_g, h=None, prev=current)

            # Skip if duplicate with better/equal path
            if duplicate_in_open(new_node, open_set):
                continue
            if duplicate_in_closed(new_node, closed_set):
                continue

            # Only now compute heuristic (node will be kept)
            new_node.h = heuristic(neighbor)

            add_to_open(new_node, open_set)

    return None  # no solution
