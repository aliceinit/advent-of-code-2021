from queue import Queue
from collections import deque

transform_functions = [
    # # Face z
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (y, -x, z),

    # Face -z
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (y, x, -z),
    #
    # # Face x
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (y, z, x),
    #
    # # Face -x
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (-z, -y, -x),
    lambda x, y, z: (y, -z, -x),

    # # Face y
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (-z, -x, y),

    # # Face -y
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (-z, x, -y)
]


class Beacon:

    def __init__(self, x, y, z):
        self.position = (x, y, z)
        self.relative_neighbours = []

    def __repr__(self):
        return str(self.position)

    def add_neighbour(self, x, y, z):
        relative_point = (self.position[0] - x,
                          self.position[1] - y,
                          self.position[2] - z)
        self.relative_neighbours.append(relative_point)

    def check_match(self, other):
        """
        Compare to another point; they match if we find at least 11 shared relative neighbours
        repeat with transformations to account for scanner alignment
        return boolean (match found?) and a transform function (if match found) to convert points from
        other to the same schema as self.
        """
        for fn in transform_functions:
            remaining_neighbours = len(other.relative_neighbours)
            matching_neighbours = 0
            neighbour_queue = Queue()
            for other_n in other.relative_neighbours:
                neighbour_queue.put(fn(*other_n))

            while remaining_neighbours + matching_neighbours > 10:
                potential_match = neighbour_queue.get()
                if potential_match in self.relative_neighbours:
                    matching_neighbours += 1

                if matching_neighbours > 10:
                    print(f"{other.position} == {self.position} => {fn(*self.position)}")
                    return True, fn
                else:
                    remaining_neighbours -= 1
        return False, None


class Scanner:

    def __init__(self, name):
        self.name = name
        self.beacons = []
        self.other_scanners = []

    def add_beacon(self, x, y, z):
        new_beacon = Beacon(x, y, z)
        for c in self.beacons:
            new_beacon.add_neighbour(*c.position)
            c.add_neighbour(*new_beacon.position)

        self.beacons.append(new_beacon)
        return new_beacon

    def add_beacons(self, beacons, fn):
        self.other_scanners.append(fn(0, 0, 0))
        original_beacons = [b.position for b in self.beacons]
        duplicate_beacons = []
        for x, y, z in [fn(*b.position) for b in beacons]:
            if (x, y, z) in original_beacons:
                duplicate_beacons.append((x, y, z))
            else:
                self.add_beacon(x, y, z)
        return duplicate_beacons

    def __repr__(self):
        s = f"--- {self.name}---\n"
        for b in self.beacons:
            s += str(b) + "\n"
        return s


def build_scanner_transform_function(beacon_1, beacon_2, face_fn):
    x2, y2, z2 = face_fn(*beacon_2.position)
    x_diff = beacon_1.position[0] - x2
    y_diff = beacon_1.position[1] - y2
    z_diff = beacon_1.position[2] - z2

    def fn(x, y, z):
        x, y, z = face_fn(x, y, z)
        x += x_diff
        y += y_diff
        z += z_diff
        return x, y, z

    return fn


def find_beacon_overlap(s1: Scanner, s2: Scanner):
    for b1 in s1.beacons:
        for b2 in s2.beacons:
            eq, fn = b1.check_match(b2)
            if eq:
                transform_function = build_scanner_transform_function(b1, b2, fn)
                print(f"Transform: {b2.position} => {transform_function(*b2.position)}")
                return True, s1.add_beacons(s2.beacons, transform_function)
    return False, []


def find_largest_scanner_distance(scanner: Scanner):
    largest_distance = 0
    scanner_positions = scanner.other_scanners + [(0, 0, 0)]
    for s1 in scanner_positions:
        for s2 in scanner_positions:
            if s1 != s2:
                distance = sum([
                    abs(s1[0] - s2[0]),
                    abs(s1[1] - s2[1]),
                    abs(s1[2] - s2[2])
                ])
                if distance > largest_distance:
                    print(f"{s1} - {s2} => {distance}")
                    largest_distance = distance
    return largest_distance


def join_scanners(scanners):
    unified_scanner = scanners[0]
    scanner_queue = deque()

    # This would be faster if i joined random pairs together and parallelized ...

    for s in scanners[1:]:
        scanner_queue.append(s)
    while len(scanner_queue) > 0:
        s = scanner_queue.popleft()
        print(f"Trying to merge {s.name}")
        matched, _ = find_beacon_overlap(unified_scanner, s)
        if not matched:
            scanner_queue.append(s)
        else:
            print(f"Found overlap between {unified_scanner.name} and {s.name}")
    return unified_scanner


def parse_beacons(file):
    lines = [l.strip() for l in file.readlines()]
    scanners = []
    for l in lines:

        if l.startswith("---"):
            scanners.append(Scanner(l.split("---")[1].strip()))
        elif len(l) > 0:
            scanners[-1].add_beacon(*[int(c) for c in l.split(",")])

    return scanners


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        scanners = parse_beacons(f)
        unified_scanner = join_scanners(scanners)
        print(f"Joined space has {len(unified_scanner.beacons)} beacons")
        largest_distance = find_largest_scanner_distance(unified_scanner)
        print(f"The largest distance between two beacons is {largest_distance}")
