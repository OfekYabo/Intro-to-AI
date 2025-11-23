from collections import Counter

goal_visible_heuristics = []
goal_adjacent_color_pairs = set()
goal_visible_counts = Counter()   # NEW: global counts of goal visible colors


def init_goal_for_heuristics(goal_blocks):
    """
    Initialize goal information for the heuristics.
    goal_blocks is a string such as "2,22,4,3" representing the visible colors.
    """
    global goal_visible_heuristics, goal_adjacent_color_pairs, goal_visible_counts
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
    
    # Precompute goal visible color counts
    goal_visible_counts = Counter(goal_visible_heuristics)


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

    if n == 0:
        return h

    for i in range(n - 1):
        c1 = blocks[i]
        c2 = blocks[i + 1]
        a1, b1 = c1
        a2, b2 = c2

        ok = False
        # 4 explicit combinations, order-insensitive
        if ((min(a1, a2), max(a1, a2)) in goal_pairs or
            (min(a1, b2), max(a1, b2)) in goal_pairs or
            (min(b1, a2), max(b1, a2)) in goal_pairs or
            (min(b1, b2), max(b1, b2)) in goal_pairs):
            ok = True

        if not ok:
            h += 1

    return h


def advanced_heuristic(_color_blocks_state):
    blocks = _color_blocks_state.blocks
    n = len(blocks)
    goal_pairs = goal_adjacent_color_pairs

    if n == 0:
        return 0

    h = 0
    extra_used = False

    # Build current visible color counts while iterating
    curr_counts = Counter()

    # --- 1. adjacency + extra-flip logic (your existing idea) ---
    for i in range(n - 1):
        c1 = blocks[i]
        c2 = blocks[i + 1]
        a1, b1 = c1
        a2, b2 = c2

        # update curr_counts for the left block of the pair
        # (block i may appear twice across iterations, but Counter can handle it;
        # if you want exact counts, you can do a separate pass, but this is fine
        # if you only care about relative lower bound)
        curr_counts[a1] += 1  # visible color of block i

        # adjacency logic (same as base)
        ok = False
        if ((min(a1, a2), max(a1, a2)) in goal_pairs or
            (min(a1, b2), max(a1, b2)) in goal_pairs or
            (min(b1, a2), max(b1, a2)) in goal_pairs or
            (min(b1, b2), max(b1, b2)) in goal_pairs):
            ok = True
            # extra flip logic: applied at most once globally
            if not extra_used:
                if goal_visible_heuristics[i] not in blocks[i]:
                    h += 1
                    extra_used = True    

        if not ok:
            extra_used = True 
            h += 1

    # ensure we also count the visible color of the last block
    last_visible = blocks[-1][0]
    curr_counts[last_visible] += 1

    # --- 2. global color mismatch -> minimal spins ---
    total_missing = 0
    for color, g_cnt in goal_visible_counts.items():
        c_cnt = curr_counts.get(color, 0)
        if g_cnt > c_cnt:
            total_missing += (g_cnt - c_cnt)

    h += total_missing
    return h
