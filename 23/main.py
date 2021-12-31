from queue import PriorityQueue
from collections import namedtuple


class BurrowSpace:
    def __init__(self, x, y, name="", depth=0):
        self.x = x
        self.y = y
        self.room_name: str = name
        self.room_depth: int = depth
        self.left: BurrowSpace = None
        self.right: BurrowSpace = None
        self.down: BurrowSpace = None
        self.up: BurrowSpace = None

    def is_hallway(self):
        return self.up is None

    def is_room(self):
        return self.up is not None

    def is_room_entry(self):
        """ Is this a space immediately outside a room?"""
        return self.up is None and self.down is not None


class Burrow:
    energy_table = {"A": 1,
                    "B": 10,
                    "C": 100,
                    "D": 1000}
    x_to_letter = {3: "A",
                   5: "B",
                   7: "C",
                   9: "D"}
    letter_to_x = {v: k for k, v in x_to_letter.items()}

    def __init__(self, burrow_str):
        self.initial_amphipods = {}
        self.burrow = []

        for y, row in enumerate(burrow_str.split("\n")):
            self.burrow.append([])
            for x, char in enumerate(row):

                if char in (".", "A", "B", "C", "D"):
                    space = BurrowSpace(x, y, name=self.x_to_letter.get(x, ""), depth=y - 1)
                    self.burrow[y].append(space)
                    if y > 0:
                        up = self.burrow[y - 1][x]
                        if up is not None:
                            space.up = up
                            up.down = space
                    if x > 0:
                        left = self.burrow[y][x - 1]
                        if left is not None:
                            space.left = left
                            left.right = space
                    if char in ("A", "B", "C", "D"):
                        self.initial_amphipods[(x, y)] = char
                else:
                    self.burrow[y].append(None)

    def is_organized(self, amphipods):
        for coords, letter in amphipods.items():
            x, y = coords
            b: BurrowSpace = self.burrow[y][x]
            if letter != b.room_name:
                return False
        return True

    def organize(self):

        # sort queue by total expended energy; first to finish is shortest
        visited_burrow_states = set()
        burrow_states = PriorityQueue()

        class State:
            parent: Burrow = self

            def __init__(self, energy, amphipods):
                self.energy = energy
                self.amphipods = amphipods

            def __lt__(self, other):
                return self.energy < other.energy

            def __repr__(self):
                b = f"Energy used: {self.energy}\n---------------------"
                for y, row in enumerate(self.parent.burrow):
                    b += "\n"
                    for x, space in enumerate(row):
                        if space is not None:
                            a = self.amphipods.get((x, y))
                            if a:
                                b += a
                            else:
                                b += "."
                        else:
                            b += "#"

                return b

        def make_save_state(s: State):
            return (
                s.energy,
                tuple(
                    sorted(
                        [(coord[0], coord[1], letter) for coord, letter in s.amphipods.items()]
                    )
                )
            )

        burrow_states.put(State(0, {k: v for k, v in self.initial_amphipods.items()}))

        while not burrow_states.empty():
            state: State = burrow_states.get()

            if self.is_organized(state.amphipods):
                return state.energy, state.amphipods

            # next states should all include moving amphipods home where possible
            home_energy = self.move_amphipods_home(state.amphipods)
            while home_energy > 0:
                state.energy += home_energy
                home_energy = self.move_amphipods_home(state.amphipods)

            if self.is_organized(state.amphipods):
                # Even though we found a solution, it may not be minimal
                # Put it back in the priority queue
                if make_save_state(state) not in visited_burrow_states:
                    burrow_states.put(state)

            # Get possible next states & energy needed to get to each
            next_states = self.find_all_moves_to_hallway(state.amphipods)
            for e, positions in next_states:
                next_state = State(state.energy + e, positions)
                if make_save_state(next_state) not in visited_burrow_states:
                    burrow_states.put(next_state)
            visited_burrow_states.add(make_save_state(state))

    def move_amphipods_home(self, amphipod_positions):
        """
        For any amphipod that can reach its destination, move it there
        Updates amphipod position map and returns energy expended to move amphipods
        """
        energy_expended = 0
        original_positions = {k: v for k, v in amphipod_positions.items()}

        def get_space_letter(s):
            return amphipod_positions.get((s.x, s.y))

        ready_rooms = set(self.x_to_letter.values())

        # Determine which rooms are ready to accept occupants
        for row in self.burrow:
            for space in row:
                space: BurrowSpace = space
                if space is not None and space.room_name in ready_rooms and space.room_depth > 0:
                    occupant = get_space_letter(space)
                    if occupant and occupant != space.room_name:
                        ready_rooms.remove(space.room_name)

        # if no rooms are ready, return early
        if len(ready_rooms) == 0:
            return energy_expended

        for coords, letter in original_positions.items():
            if letter not in ready_rooms:
                # Only consider amphipods whose rooms are ready to accept correct occupants
                continue

            x, y = coords
            space: BurrowSpace = self.burrow[y][x]

            # Is the amphipod in the right room? It is either organized OR cannot move home
            # on this step (needs to unblock a neighbour)
            if space.room_name == letter:
                continue

            step_counter = 0
            move_left = space.x > self.letter_to_x.get(letter)
            current_space = space
            if space.is_room():
                next_space = space.up
            elif move_left:
                next_space = space.left
            else:
                next_space = space.right

            while next_space is not None and not get_space_letter(next_space):
                step_counter += 1
                current_space = next_space
                if current_space.is_room() and current_space.room_name != letter:
                    next_space = current_space.up
                elif current_space.down and current_space.down.room_name == letter:
                    next_space = current_space.down
                elif move_left:
                    next_space = current_space.left
                else:
                    next_space = current_space.right

            if current_space.room_name == letter:
                amphipod_positions.pop((space.x, space.y))
                amphipod_positions[(current_space.x, current_space.y)] = letter
                energy_expended += step_counter * self.energy_table.get(letter)

        return energy_expended

    def find_all_moves_to_hallway(self, amphipod_positions):
        """
        Find all possible moves to hallway from rooms
        return a list of tuples (energy required, next possible positions)
        """
        possible_moves = []

        def get_space_letter(s):
            return amphipod_positions.get((s.x, s.y))

        for coords, letter in amphipod_positions.items():
            x, y = coords

            space: BurrowSpace = self.burrow[y][x]
            if not space.is_room():
                continue  # We are already in a hallway

            if get_space_letter(space.up):
                continue  # We can't move if somebody is above us

            # We won't move if we are in our destination & so are all downward neighbours
            if letter == space.room_name:
                is_home = True
                downward_neighbour = space.down
                while downward_neighbour:
                    if downward_neighbour.room_name != get_space_letter(downward_neighbour):
                        is_home = False
                    downward_neighbour = downward_neighbour.down
                if is_home:
                    continue

            # We can move!
            step_count = 0

            # Since we always start from a room, start moving up
            current_space: BurrowSpace = space
            next_space: BurrowSpace = current_space.up
            branch_space = None
            steps_at_branch = 0
            move_left = True

            while next_space and not get_space_letter(next_space):
                step_count += 1

                # Set a branch point when we hit the hallway
                if current_space.is_room() and next_space.is_hallway():
                    branch_space = next_space
                    steps_at_branch = step_count

                current_space = next_space

                # Check if we are in a valid destination
                if current_space.is_hallway() and not current_space.is_room_entry():
                    next_positions = {k: v for k, v in amphipod_positions.items()}
                    next_positions.pop((space.x, space.y))
                    next_positions[(current_space.x, current_space.y)] = letter
                    possible_moves.append((step_count * self.energy_table.get(letter), next_positions))

                if current_space.is_room():
                    next_space = current_space.up
                elif move_left:
                    next_space = current_space.left
                    # If we hit a blocker on left path, switch to right path
                    if not next_space or get_space_letter(next_space):
                        current_space = branch_space
                        next_space = current_space.right
                        step_count = steps_at_branch
                        move_left = False
                else:
                    next_space = current_space.right
        return possible_moves


def parse_amphipod_burrow(file):
    return Burrow(file.read())


def parse_unfolded_amphipod_burrow(file):
    lines = file.readlines()
    new_str = "".join(lines[0:-2] + ["  #D#C#B#A#\n", "  #D#B#A#C#\n"] + lines[-2:])
    return Burrow(new_str)


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        burrow = parse_amphipod_burrow(f)
        e, _ = burrow.organize()
        print(f"First burrow: took {e} energy")
    with open("puzzle_1_input.text", "r") as f:
        unfolded = parse_unfolded_amphipod_burrow(f)
        e, _ = unfolded.organize()
        print(f"Full burrow: took {e} energy")

