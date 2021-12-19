from heapdict import heapdict


class CavePosition:
    def __init__(self, x, y, risk):
        self.name = f"{x},{y}"
        self.node_risk = risk
        self.total_risk = 999999999999999
        self.neighbours = set()
        self.visited = False

    def add_neighbour(self, p):
        self.neighbours.add(p)
        p.neighbours.add(self)

    def __repr__(self):
        return f"{self.name}: {self.node_risk} (total = {self.total_risk}, visited = {self.visited})"


def find_best_path(start_node: CavePosition, goal_node: CavePosition, ):
    """
    finds the lowest risk path from top left to bottom right
    and returns the sum of the risk scores for each point on the path
    """
    unvisited = heapdict({start_node: 0})
    start_node.total_risk = 0
    current_node = start_node
    while current_node is not goal_node:
        for n in current_node.neighbours:
            n: CavePosition
            current_risk = n.total_risk
            new_risk = current_node.total_risk + n.node_risk
            if new_risk < current_risk:
                n.total_risk = new_risk
                if unvisited.get(n):
                    unvisited[n] = n.total_risk
            if not n.visited is True:
                unvisited[n] = n.total_risk
        try:
            unvisited.pop(current_node)
        except KeyError:
            pass
        current_node.visited = True
        current_node, _ = unvisited.popitem()
    return goal_node.total_risk


def parse_cave_paths(file):
    position_list = [
        [int(i) for i in line.strip()]
        for line in file.readlines()
    ]
    max_y = len(position_list) - 1
    max_x = len(position_list[0]) - 1
    nodes = []

    for y, row in enumerate(position_list):
        nodes.append([])
        for x, risk in enumerate(row):
            new_node = CavePosition(x, y, risk)
            nodes[-1].append(new_node)

            # Connect to nodes up and left, if within bounds
            potential_connections = (("up", y - 1, x), ("left", y, x - 1))
            for direction, neighbour_y, neighbour_x in potential_connections:

                if neighbour_x >= 0 and neighbour_y >= 0:
                    new_node.add_neighbour(nodes[neighbour_y][neighbour_x])
    return nodes[0][0], nodes[max_y][max_x]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        nodes = parse_cave_paths(f)
        least_score = find_best_path(*nodes)
        print(f"Lowest possible path risk = {least_score}")
