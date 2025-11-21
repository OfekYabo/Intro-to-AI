from color_blocks_state import color_blocks_state

goal_visible_heuristics = []
goal_adjacent_color_pairs = set()


def init_goal_for_heuristics(goal_blocks):
    """
    Initialize goal information for the heuristics.
    goal_blocks is a string such as "2,22,4,3" representing the visible colors.
    """
    global goal_visible_heuristics, goal_adjacent_color_pairs
    goal_visible_heuristics = []
    for part in goal_blocks.split(','):
        part = part.strip()
        if part:
            goal_visible_heuristics.append(int(part))

    # Build all adjacent visible-color pairs from the goal state
    goal_adjacent_color_pairs = set()
    for i in range(len(goal_visible_heuristics) - 1):
        col1 = goal_visible_heuristics[i]
        col2 = goal_visible_heuristics[i + 1]
        pair = (col1, col2) if col1 <= col2 else (col2, col1)  # order doesn’t matter
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
    goal_pairs = goal_adjacent_color_pairs  # local alias

    for i in range(n - 1):
        c1 = blocks[i]
        c2 = blocks[i + 1]

        ok = False
        for col1 in c1:
            for col2 in c2:
                pair = (col1, col2) if col1 <= col2 else (col2, col1)
                if pair in goal_pairs:
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
    2) Add: small bonus from the top - if the top visible color is wrong -> +1

    The top check is conservative (only the first block) to stay admissible
    while still nudging the search toward aligning the tower from the top.
    """

    blocks = _color_blocks_state.blocks

    # base adjacency heuristic 
    h = base_heuristic(_color_blocks_state)

    #   bottom   
    if goal_visible_heuristics and blocks:
        bottom_visible = blocks[-1][0]
        if bottom_visible != goal_visible_heuristics[-1]:
            h += 1

    return h
