from collections import Counter

goal_visible_heuristics = []
goal_adjacent_color_pairs = set()
goal_visible_counts = Counter()   # counts of goal visible colors


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


def _norm_pair(x, y):
    """Return ordered pair (min,max) without calling min()/max() twice."""
    if x <= y:
        return (x, y)
    return (y, x)


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
    blocks = _color_blocks_state.blocks
    n = len(blocks)
    if n == 0:
        return 0

    goal_pairs = goal_adjacent_color_pairs  # local alias
    h = 0

    for i in range(n - 1):
        a1, b1 = blocks[i]
        a2, b2 = blocks[i + 1]

        # 4 explicit combinations, order-insensitive, using _norm_pair
        p1 = _norm_pair(a1, a2)
        p2 = _norm_pair(a1, b2)
        p3 = _norm_pair(b1, a2)
        p4 = _norm_pair(b1, b2)

        if not (p1 in goal_pairs or p2 in goal_pairs or p3 in goal_pairs or p4 in goal_pairs):
            h += 1

    return h


def advanced_heuristic(_color_blocks_state):
    blocks = _color_blocks_state.blocks
    n = len(blocks)
    if n == 0:
        return 0

    goal_pairs = goal_adjacent_color_pairs
    goal_vis = goal_visible_heuristics
    goal_counts = goal_visible_counts

    # --- 0. build current visible color counts in one pass ---
    curr_counts = Counter(a for (a, b) in blocks)

    h = 0
    extra_flip = False

    # --- 1. adjacency + extra-flip logic (your idea) ---
    for i in range(n - 1):
        a1, b1 = blocks[i]
        a2, b2 = blocks[i + 1]

        # adjacency logic (same as base but using _norm_pair)
        ok = False
        p1 = _norm_pair(a1, a2)
        p2 = _norm_pair(a1, b2)
        p3 = _norm_pair(b1, a2)
        p4 = _norm_pair(b1, b2)
        if (p1 in goal_pairs or p2 in goal_pairs or p3 in goal_pairs or p4 in goal_pairs):
            ok = True
            # extra flip logic: applied at most once globally
            if not extra_flip:
                required = goal_vis[i]
                if required != a1 and required != b1:
                    h += 1
                    extra_flip = True

        if not ok:
            h += 1
            extra_flip = True

    # --- 2. global color mismatch minimal spins ---
    total_missing = 0
    for color, g_cnt in goal_counts.items():
        c_cnt = curr_counts.get(color, 0)
        if g_cnt > c_cnt:
            total_missing += (g_cnt - c_cnt)

    h += total_missing
    return h
