class Instruction:
    def __init__(self, op, min_x, max_x, min_y, max_y, min_z, max_z):

        # keep real min and max
        self.min_x = min([min_x, max_x])
        self.max_x = max([min_x, max_x])
        self.min_y = min([min_y, max_y])
        self.max_y = max([min_y, max_y])
        self.min_z = min([min_z, max_z])
        self.max_z = max([min_z, max_z])

        if isinstance(op, str):
            self.op = True if op == "on" else False
            self.max_x += 1
            self.max_y += 1
            self.max_z += 1
        else:
            self.op = op

        self.is_init_instruction = (self.min_x >= -50 and
                                    self.min_y >= -50 and
                                    self.min_z >= -50 and
                                    self.max_x <= 51 and
                                    self.max_y <= 51 and
                                    self.max_z <= 51)

    def __repr__(self):
        return f"{self.op} " + \
               f"x={self.min_x}..{self.max_x}," + \
               f"y={self.min_y}..{self.max_y}," + \
               f"z={self.min_z}..{self.max_z}"

    def get_size(self):
        return ((self.max_x - self.min_x)
                * (self.max_y - self.min_y)
                * (self.max_z - self.min_z))


class InstructionSet:
    """Maintains a set of non-overlapping instructions"""

    def __init__(self):
        self.instructions = []

    def count_on_cubes(self):
        count = 0
        for i in self.instructions:
            if i.op is True:
                count += i.get_size()
        return count

    def add_instruction(self, instruction: Instruction):
        """
        Adds new instruction while breaking down new or existing instructions
        into non-overlapping regions
        """
        updated = []
        for index, i1 in enumerate(self.instructions):
            new_instructions = self.merge_instructions(i1, instruction)
            updated += new_instructions
        if instruction.op is True:
            updated += [instruction]

        self.instructions = updated

    def merge_instructions(self, i1: Instruction, i2: Instruction):
        previous_instruction = []
        overlap_area: Instruction = self.find_overlap(i1, i2)
        if overlap_area is None:
            return [i1]
        previous_instruction += self.split_instruction(i1, overlap_area)

        return previous_instruction

    @staticmethod
    def split_instruction(i: Instruction, overlap: Instruction):
        split = [
            # Add space to the left of the overlap area
            Instruction(i.op,
                        i.min_x, overlap.min_x,
                        i.min_y, i.max_y,
                        i.min_z, i.max_z),
            # Add remaining space above the overlap area
            Instruction(i.op,
                        overlap.min_x, i.max_x,
                        overlap.max_y, i.max_y,
                        i.min_z, i.max_z),
            # Add remaining space to the right of overlap area
            Instruction(i.op,
                        overlap.max_x, i.max_x,
                        i.min_y, overlap.max_y,
                        i.min_z, i.max_z),
            # Add remaining space in front of the overlap area
            Instruction(i.op,
                        overlap.min_x, overlap.max_x,
                        i.min_y, overlap.max_y,
                        i.min_z, overlap.min_z),
            # Add remaining space behind the overlap area
            Instruction(i.op,
                        overlap.min_x, overlap.max_x,
                        i.min_y, overlap.max_y,
                        overlap.max_z, i.max_z),
            # Add remaining space underneath the overlap area
            Instruction(i.op,
                        overlap.min_x, overlap.max_x,
                        i.min_y, overlap.min_y,
                        overlap.min_z, overlap.max_z)]
        new_split = []
        for s in split:
            if s.get_size() > 0:
                new_split.append(s)
        return new_split

    @staticmethod
    def find_overlap(i1: Instruction, i2: Instruction):
        if all([
            (i1.min_x <= i2.min_x <= i1.max_x
             or i1.min_x <= i2.max_x <= i1.max_x
             or i2.min_x <= i1.min_x <= i2.max_x
             or i2.min_x <= i1.max_x <= i2.max_x),
            (i1.min_y <= i2.min_y <= i1.max_y
             or i1.min_y <= i2.max_y <= i1.max_y
             or i2.min_y <= i1.min_y <= i2.max_y
             or i2.min_y <= i1.max_y <= i2.max_y),
            (i1.min_z <= i2.min_z <= i1.max_z
             or i1.min_z <= i2.max_z <= i1.max_z
             or i2.min_z <= i1.min_z <= i2.max_z
             or i2.min_z <= i1.max_z <= i2.max_z)
        ]):
            x_vals = sorted([i1.min_x, i1.max_x, i2.min_x, i2.max_x])
            y_vals = sorted([i1.min_y, i1.max_y, i2.min_y, i2.max_y])
            z_vals = sorted([i1.min_z, i1.max_z, i2.min_z, i2.max_z])
            overlap = Instruction(i2.op,
                                  x_vals[1], x_vals[2],
                                  y_vals[1], y_vals[2],
                                  z_vals[1], z_vals[2])
            if overlap.get_size() > 0:
                return overlap


def perform_reboot(instructions, full_reboot=False):
    instruction_set = InstructionSet()

    for i in instructions:
        if full_reboot or i.is_init_instruction:
            instruction_set.add_instruction(i)

    return instruction_set.count_on_cubes()


def parse_reboot_instructions(file):
    lines = [l.strip() for l in file.readlines()]
    instructions = []
    for l in lines:
        op, coords = l.split(" ")
        x, y, z = coords.split(",")
        x_min, x_max = x.split("..")
        y_min, y_max = y.split("..")
        z_min, z_max = z.split("..")
        instructions.append(Instruction(op,
                                        int(x_min[2:]), int(x_max),
                                        int(y_min[2:]), int(y_max),
                                        int(z_min[2:]), int(z_max)))

    return instructions


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        instructions = parse_reboot_instructions(f)
        on_cubes = perform_reboot(instructions)
        print(f"After init, {on_cubes} cubes are on!")

        on_cubes = perform_reboot(instructions, full_reboot=True)
        print(f"After reboot, {on_cubes} cubes are on!")