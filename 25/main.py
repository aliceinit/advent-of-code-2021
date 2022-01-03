class OceanFloorIterator:
    def __init__(self, initial_space):
        self.space = initial_space

    def __next__(self):
        if self.space is None:
            raise StopIteration
        next_space = self.space.right
        if next_space.x == 0:
            next_space = next_space.down
            if next_space.y == 0:
                next_space = None
        space = self.space
        self.space = next_space
        return space


class OceanFloorSpace:
    def __init__(self, x, y, initial_state):
        if initial_state not in [".", ">", "v"]:
            raise AttributeError(f"Invalid ocean floor space: {initial_state}")
        self.x = x
        self.y = y
        self.state = initial_state
        self.next_state = None
        self.right = None
        self.down = None

    def __repr__(self):
        rows = []
        for s in self:
            if len(rows) - 1 < s.y:
                rows.append("")
            rows[s.y] += s.state
        rows = ["-"*(len(rows[0]) + 3)] + rows + ["-"*(len(rows[0]) + 3)]
        return "\n".join(rows)

    def __iter__(self):
        return OceanFloorIterator(self)

    def update_state(self):
        if self.next_state:
            self.state = self.next_state
            self.next_state = None


def move_cucumbers(ocean_floor):
    east_cucumber_updates = []
    south_cucumber_updates = []

    # find and update all east cucumbers
    for floor in ocean_floor:
        if floor.state == ">":
            # check if we can move right
            if floor.right.state == ".":
                floor.next_state = "."
                floor.right.next_state = ">"
                east_cucumber_updates += [floor, floor.right]
    for cucumber in east_cucumber_updates:
        cucumber.update_state()

    # find and update all south cucumbers
    for floor in ocean_floor:
        if floor.state == "v":
            # check if we can move down
            if floor.down.state == ".":
                floor.next_state = "."
                floor.down.next_state = "v"
                south_cucumber_updates += [floor, floor.down]
    for cucumber in south_cucumber_updates:
        cucumber.update_state()

    return len(east_cucumber_updates) > 0 \
           or len(south_cucumber_updates) > 0  # Indicate to caller whether we are deadlocked


def move_cucumbers_until_deadlock(ocean_floor):
    move_count = 0
    moved = move_cucumbers(ocean_floor)
    while moved:
        move_count += 1
        moved = move_cucumbers(ocean_floor)
        print(f"Iteration {move_count}: {moved}")
    return move_count


def parse_ocean_floor(file):
    lines = [l.strip() for l in file.readlines()]
    spaces = []
    for y, row in enumerate(lines):
        spaces.append([])
        for x, char in enumerate(row):
            c = OceanFloorSpace(x, y, char)
            spaces[y].append(c)
            # link self to left neighbour
            if x > 0:
                left = spaces[y][x - 1]
                left.right = c
            # link self to upper neighbour
            if y > 0:
                up = spaces[y - 1][x]
                up.down = c

    # Link top row as downward neighbour of bottom row
    for x in range(0, len(spaces[0])):
        top_row = spaces[0][x]
        bottom_row = spaces[len(spaces) - 1][x]
        bottom_row.down = top_row

    # Link left column as rightward neighbour of right column
    for y in range(0, len(spaces)):
        left_column = spaces[y][0]
        right_column = spaces[y][len(spaces[0]) - 1]
        right_column.right = left_column
    return spaces[0][0]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        ocean_floor = parse_ocean_floor(f)
        rounds = move_cucumbers_until_deadlock(ocean_floor)
        print(f"Cucumbers stop moving after {rounds + 1} rounds")
