class SnailNumber:

    def __init__(self, value=None):
        self.left = None
        self.right = None
        self.value = value
        self.parent = None

    def __repr__(self):
        if self.value is not None:
            return f"{self.value}"
        else:
            return f"[{self.left},{self.right}]"

    def add_left(self, child):
        self.left = child
        self.left.parent = self

    def add_right(self, child):
        self.right = child
        self.right.parent = self

    @staticmethod
    def from_str(number_str):
        nums = []
        int_accumulator = ""
        for c in number_str:
            if c == "[":
                nums.append(SnailNumber())
            elif c == ",":
                if int_accumulator:
                    nums.append(SnailNumber(int(int_accumulator)))
                    int_accumulator = ""
            elif c == "]":
                if int_accumulator:
                    nums.append(SnailNumber(int(int_accumulator)))
                    int_accumulator = ""
                nums[-3].add_left(nums[-2])
                nums[-3].add_right(nums[-1])
                nums = nums[:-2]
            else:  # number
                int_accumulator += c
        return nums[0]

    def get_magnitude(self):
        if self.value:
            return self.value
        elif self.left and self.right:
            return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()
        else:
            return 0

    def sum(self, snail_number):
        """Return a new snail number that is the sum of self + another snail number"""
        sn = SnailNumber()
        sn.add_left(self)
        sn.add_right(snail_number)
        sn.reduce()
        return sn

    def find_next_left_val(self):
        # go up the parent chain until we are not the left branch
        branch = self
        parent = self.parent
        while parent is not None:
            if parent.left == branch:
                # We are coming from the left branch; keep going up
                branch = parent
                parent = parent.parent
            else:
                break
        if not parent:
            # No number exists to the left of us
            return
        # Follow the next left branch from shared parent
        left_val = parent.left

        # Find the right-most child of the left branch
        while left_val.value is None:
            left_val = left_val.right
        return left_val

    def find_next_right_val(self):
        # go up the parent chain until we are not the right branch
        branch = self
        parent = self.parent
        while parent is not None:

            if parent.right == branch:
                # We are coming from the right branch; keep going up
                branch = parent
                parent = parent.parent
            else:
                break
        if not parent:
            # No number exists to the right of us
            return
        # Follow the next right branch from shared parent
        right_val = parent.right

        # Find the left-most child of the left branch
        while right_val.value is None:
            right_val = right_val.left
        return right_val

    def explode(self, depth=0):
        if depth >= 4 and not self.value and self.left and self.right:
            # Problem states these will always be leaf nodes
            l = self.left.value
            r = self.right.value

            next_left = self.left.find_next_left_val()
            if next_left:
                next_left.value += l

            next_right = self.right.find_next_right_val()

            if next_right:
                next_right.value += r

            # Transform self into a leaf node
            self.value = 0
            self.left = None
            self.right = None
            return True  # We did an explode operation
        elif self.value is not None:
            return False
        else:
            return ((self.left and self.left.explode(depth=depth + 1))
                    or (self.right and self.right.explode(depth=depth + 1)))

    def copy(self):
        return SnailNumber.from_str(str(self))

    def split(self):
        if self.value is not None:
            if self.value < 10:
                return False
            else:
                # Split value
                left = int(self.value / 2)
                right = int(self.value / 2) if self.value % 2 == 0 else int(self.value / 2) + 1
                self.value = None
                self.add_left(SnailNumber(left))
                self.add_right(SnailNumber(right))
                return True
        else:
            return ((self.left and self.left.split())
                    or (self.right and self.right.split()))

    def reduce(self):
        is_reduced = False

        while not is_reduced:
            exploded = self.explode()
            if not exploded:
                split = self.split()
                if not split:
                    is_reduced = True


def snail_sum(snail_numbers):
    snail_sum = snail_numbers[0]
    for sn in snail_numbers[1:]:
        snail_sum = snail_sum.sum(sn)

    return snail_sum


def find_largest_sum_of_two(snail_numbers):
    largest_sum = SnailNumber(0)
    sn1 = None
    sn2 = None
    for x in snail_numbers:
        for y in snail_numbers:
            if x != y:
                xy_sum = x.copy().sum(y.copy())
                if xy_sum.get_magnitude() > largest_sum.get_magnitude():
                    largest_sum = xy_sum
                    sn1 = x
                    sn2 = y
    return largest_sum


def parse_snail_homework(file):
    lines = [l.strip() for l in file.readlines()]
    return [SnailNumber.from_str(l) for l in lines]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        homework = parse_snail_homework(f)
        final_sum = snail_sum(homework)
        print(f"Final homework answer:{final_sum}")
        print(f"\t magnitude = {final_sum.get_magnitude()}")

    with open("puzzle_1_input.text", "r") as f:
        homework = parse_snail_homework(f)
        largest_sum_of_two = find_largest_sum_of_two(homework)
        print(F"Largest sum of two = {largest_sum_of_two.get_magnitude()}")
