from color_blocks_state import color_blocks_state

goal_visible = []
goal_adjacent_color_pairs = set()


def init_goal_for_heuristics(goal_blocks):
    """
    Initialize goal information for the heuristics.
    goal_blocks is a string such as "2,22,4,3" representing the visible colors.
    """
    global goal_visible, goal_adjacent_color_pairs
    goal_visible = []
    for part in goal_blocks.split(','):
        part = part.strip()
        if part:
            goal_visible.append(int(part))

    # Build all adjacent visible-color pairs from the goal state
    goal_adjacent_color_pairs = set()
    for i in range(len(goal_visible) - 1):
        a = goal_visible[i]
        b = goal_visible[i + 1]
        pair = tuple(sorted((a, b)))  # order doesn’t matter
        goal_adjacent_color_pairs.add(pair)


def base_heuristic(_color_blocks_state):
    """
    For each adjacent pair of blocks in the current state:

      - Consider all 4 possible pairs obtained by choosing
        one color from the first block and one from the second.

      - If ANY of these candidate pairs matches an adjacent
        visible-color pair in the goal → cost = 0.

      - Otherwise → cost = 1.

    Sum the cost over all adjacent block pairs.
    """
    h = 0
    blocks = _color_blocks_state.blocks
    n = len(blocks)

    for i in range(n - 1):
        c1 = blocks[i]
        c2 = blocks[i + 1]

        ok = False
        for col1 in c1:
            for col2 in c2:
                pair = tuple(sorted((col1, col2)))
                if pair in goal_adjacent_color_pairs:
                    ok = True
                    break
            if ok:
                break

        if not ok:
            h += 1

    return h


def advanced_heuristic(_color_blocks_state):
    """
    Advanced heuristic:
    1) Start with the base heuristic (adjacency matching)
    2) Add: for each block from top to bottom:
           if visible color != goal visible color at this position -> +1
           else -> +0

    This is admissible because every mismatch requires at least one operation.
    """

    h = 0
    blocks = _color_blocks_state.blocks
    global goal_visible

    # ---- PART 1: base adjacency heuristic ----
    n = len(blocks)

    for i in range(n - 1):
        c1 = blocks[i]
        c2 = blocks[i + 1]
        ok = False
        for col1 in c1:
            for col2 in c2:
                pair = tuple(sorted((col1, col2)))
                if pair in goal_adjacent_color_pairs:
                    ok = True
                    break
            if ok:
                break
        if not ok:
            h += 1

    # ---- PART 2: top-down visible color check ----
    for i in range(len(goal_visible)):
        visible_color = blocks[i][0]
        if visible_color != goal_visible[i]:
            h += 1

    return h

