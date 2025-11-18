goal_visible_colors = []


def init_goal_for_search(goal_blocks):
    global goal_visible_colors
    # goal_blocks example: "2,22,4,3"
    # Parse the goal visible colors (this is the target tower pattern)
    goal_visible_colors = []
    for part in goal_blocks.split(','):
        part = part.strip()
        if part:
            goal_visible_colors.append(int(part))


class color_blocks_state:
    # you may add global parameters if needed

    def __init__(self, blocks_str, **kwargs):
        # If created from neighbor generation, blocks list is passed directly
        blocks = kwargs.get('blocks', None)
        if blocks is not None:
            self.blocks = [(int(a), int(b)) for (a, b) in blocks]
        else:
            # Parse from the input string
            self.blocks = []
            s = blocks_str.replace(" ", "")
            if s:
                parts = s.split('),')
                for part in parts:
                    part = part.strip()
                    if part.startswith('('):
                        part = part[1:]
                    if part.endswith(')'):
                        part = part[:-1]
                    if not part:
                        continue
                    a_str, b_str = part.split(',')
                    self.blocks.append((int(a_str), int(b_str)))

        # Canonical string representation (from top to bottom)
        

    @staticmethod
    def is_goal_state(_color_blocks_state):
        # Goal state: the visible colors match the predefined goal_visible_colors
        visible = [pair[0] for pair in _color_blocks_state.blocks]
        return visible == goal_visible_colors

    def get_neighbors(self):
        neighbors = []
        n = len(self.blocks)

        # 1. Spin operations – rotate a single block (swap its two colors)
        for i in range(n):
            new_blocks = list(self.blocks)
            a, b = new_blocks[i]
            new_blocks[i] = (b, a)
            neighbor_state = color_blocks_state("", blocks=new_blocks)
            neighbors.append((neighbor_state, 1))  # cost = 1

        # 2. Flip operations – flip a bottom sub-tower (from size 2 to n)
        for k in range(2, n + 1):
            bottom_start = n - k
            top_part = self.blocks[:bottom_start]
            sub = self.blocks[bottom_start:]

            # Reverse only the order of the blocks; do NOT swap their colors
            flipped_sub = list(reversed(sub))

            new_blocks = top_part + flipped_sub
            neighbor_state = color_blocks_state("", blocks=new_blocks)
            neighbors.append((neighbor_state, 1))

        return neighbors


    def __hash__(self):
        # Allows hashing the state (useful for sets/dicts)
        return hash(tuple(self.blocks))

    def __eq__(self, other):
        return isinstance(other, color_blocks_state) and self.blocks == other.blocks

    def get_state_str(self):
        # For debug printing
        self.state_str = ",".join(f"({a},{b})" for (a, b) in self.blocks)
        return self.state_str
