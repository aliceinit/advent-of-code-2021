def process_step(state):
    flash_count = 0

    def visit_neighbors(row, col):
        """ Check energy levels of adjacent neighbours to see if they flashed """
        neighbours = filter(lambda coord: not (
            (coord[0] == row and coord[1] == col)
            or coord[0] < 0
            or coord[1] < 0
            or coord[0] >= (len(state))
            or coord[1] >= (len(state))
        ),
                            [(row + y, col + x)
                             for x in (-1, 0, 1)
                             for y in (-1, 0, 1)])
        for r, c in neighbours:
            boost_energy(r, c)

    def boost_energy(row, col):
        new_energy = state[row][col] + 1
        state[row][col] = new_energy
        if new_energy == 10:  # Octopus just flashed
            visit_neighbors(row, col)

    for i, row in enumerate(state):
        for j in range(len(row)):
            boost_energy(i, j)

    # count flashes & reset any octopodes that flashed
    for i, row in enumerate(state):
        for j, energy_level in enumerate(row):
            if energy_level > 9:
                flash_count += 1
                state[i][j] = 0
    return flash_count


def predict_octopodes(octo_coords, steps):
    # Copy initial state instead of modifying
    flash_count = 0
    state = [[i for i in line] for line in octo_coords]
    for _ in range(0, steps):
        flash_count += process_step(state)
    return state, flash_count


def read_octopus_energy(file):
    return [
        [
            int(char)
            for char in line.strip()
        ]
        for line in file
    ]


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        octomap = read_octopus_energy(f)
        state, flashes = predict_octopodes(octomap, steps=100)
        print(f"Flashes after 100 steps: {flashes}")
