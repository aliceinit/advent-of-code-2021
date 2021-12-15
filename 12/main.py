from queue import Queue


class Cave:
    def __init__(self, name):
        self.name = name
        self.is_big = name.lower() != name
        self.connected_caves = set()

    def __repr__(self):
        return f"{self.name} ({'BIG' if self.is_big else 'small'}) --> {[c.name for c in self.connected_caves]}"


def get_all_paths(start_cave: Cave):
    paths = []
    exploration_queue = Queue()

    for next_cave in start_cave.connected_caves:
        exploration_queue.put((next_cave, [start_cave.name]))

    while not exploration_queue.empty():
        cave, partial_path = exploration_queue.get()
        if cave.name == "end":
            full_path = [name for name in partial_path] + [cave.name]
            paths.append(full_path)
        elif cave.is_big or cave.name not in partial_path:
            # This cave is a valid next step in a path
            for next_cave in cave.connected_caves:
                next_path = [name for name in partial_path] + [cave.name]
                exploration_queue.put((next_cave, next_path))

    return paths


def get_all_paths_with_double_visit(start_cave: Cave):
    paths = []
    exploration_queue = Queue()

    for next_cave in start_cave.connected_caves:
        exploration_queue.put((next_cave, [start_cave.name], False))

    while not exploration_queue.empty():
        cave, partial_path, duplicate_slot_used = exploration_queue.get()
        if cave.name == "end":
            full_path = [name for name in partial_path] + [cave.name]
            paths.append(full_path)
        elif cave.is_big or \
                (cave.name != "start" and (
                    cave.name not in partial_path or duplicate_slot_used is False
                )):
            # This cave is a valid next step in a path
            if cave.name in partial_path and not cave.is_big:
                duplicate_slot_used = True
            for next_cave in cave.connected_caves:
                next_path = [name for name in partial_path] + [cave.name]
                exploration_queue.put((next_cave, next_path, duplicate_slot_used))
    return paths


def build_cave_graph(file):
    caves_by_name = {}
    for line in file.readlines():
        cave1, cave2 = (caves_by_name.get(name, name) for name in line.strip().split("-"))

        if isinstance(cave1, str):
            cave1 = Cave(cave1)
            caves_by_name[cave1.name] = cave1
        if isinstance(cave2, str):
            cave2 = Cave(cave2)
            caves_by_name[cave2.name] = cave2

        # Connect both caves
        cave1.connected_caves.add(cave2)
        cave2.connected_caves.add(cave1)

    return caves_by_name["start"]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        cave_graph = build_cave_graph(f)
        paths = get_all_paths(cave_graph)
        print(f"Total Possible paths = {len(paths)}")
        paths_plus_one_visit = get_all_paths_with_double_visit(cave_graph)
        print(f"Total Paths allowing one extra small cave visit = {len(paths_plus_one_visit)}")