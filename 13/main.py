def perform_fold(dot_chart, fold_instruction):
    axis, index = fold_instruction
    new_dots = set()

    if axis == "x":
        # Fold right points toward the left side
        for x, y in dot_chart:
            if x > index:
                new_dots.add(
                    (index - (x - index), y)
                )
            else:
                new_dots.add((x, y))
    elif axis == "y":
        # Fold bottom rows up over top rows (Assuming no points on fold line)
        for x, y in dot_chart:
            if y > index:
                new_dots.add(
                    (x, index - (y - index))
                )
            else:
                new_dots.add((x, y))
    return new_dots


def plot_dots(dot_chart):
    max_x = 0
    max_y = 0

    for x, y in dot_chart:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            if (x, y) in dot_chart:
                line += "@"
            else:
                line += " "
        print(line)


def parse_chart_and_folds(file):
    lines = [line.strip() for line in file.readlines()]
    for i, line in enumerate(lines):
        if len(line) == 0:
            dots = set(tuple(int(n) for n in l.split(",")) for l in lines[0:i])
            instructions = []
            for l in lines[i + 1:]:
                left, right = l.split("=")
                instructions.append((left[-1], int(right)))
            return dots, instructions


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        dot_chart, fold_instructions = parse_chart_and_folds(f)
        dots = perform_fold(dot_chart, fold_instructions[0])

        print(f"Dots after one fold: {len(dots)}")

        for fold in fold_instructions[1:]:
            dots = perform_fold(dots, fold)

        print("Decoding secret code...")
        plot_dots(dots)
