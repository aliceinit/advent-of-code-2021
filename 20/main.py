class Image:

    def __init__(self, image_lines, enhancement_algorithm):
        self.min_x = 0
        self.max_x = len(image_lines[0]) - 1
        self.min_y = 0
        self.max_y = len(image_lines) - 1
        self.lit_pixels = 0
        self.pixel_map = {}
        self.default_pixel = "0"

        self.enhancement_algorithm = enhancement_algorithm

        for y, line in enumerate(image_lines):
            self.pixel_map[y] = {}
            for x, char in enumerate(line):
                if char == "#":
                    self.pixel_map[y][x] = "1"
                    self.lit_pixels += 1
                else:
                    self.pixel_map[y][x] = "0"

    def __repr__(self):
        image = ""
        for y in range(self.min_y, self.max_y + 1):
            if len(image) > 0:
                image += "\n"
            for x in range(self.min_x, self.max_x + 1):
                image += "#" if self.get_image_pixel(x, y) == "1" else "."
        return image

    def toggle_default_pixel(self):
        if self.enhancement_algorithm[int("000000000", 2)] == "1" \
                and self.enhancement_algorithm[int("111111111", 2)] == "0":
            # the 'infinite' space values toggle back and forth between 1 & 0 when we enhance
            if self.default_pixel == "0":
                self.default_pixel = "1"
            else:
                self.default_pixel = "0"

    def get_image_pixel(self, x, y):
        val = self.pixel_map.get(y, {}).get(x)
        if val is None:
            return self.default_pixel
        return val

    def set_image_pixel(self, x, y, val, pixel_map):
        if val == "1":
            self.lit_pixels += 1
            if x < self.min_x:
                self.min_x = x
            elif x > self.max_x:
                self.max_x = x

            if y < self.min_y:
                self.min_y = y
            elif y > self.max_y:
                self.max_y = y

        y_map = pixel_map.get(y)
        if y_map is None:
            pixel_map[y] = {}
        pixel_map[y][x] = val

    def enhance(self):
        """"""
        self.lit_pixels = 0
        new_pixel_map = {}
        for y in range(self.min_y - 1, self.max_y + 2):
            for x in range(self.min_x - 1, self.max_x + 2):
                pixels = [self.get_image_pixel(x=col, y=row)
                          for row in (y - 1, y, y + 1)
                          for col in (x - 1, x, x + 1)]
                index = int("".join(pixels), 2)
                enhanced_val = self.enhancement_algorithm[index]
                self.set_image_pixel(x, y, enhanced_val, new_pixel_map)
        self.pixel_map = new_pixel_map
        self.toggle_default_pixel()


def parse_enhanceable_image(file):
    algorithm = ""
    next_line = file.readline().strip()
    while next_line is not None and len(next_line) > 0:
        algorithm += next_line
        next_line = file.readline().strip()

    algorithm = ["0" if c == "." else "1" for c in algorithm]
    image = Image([l.strip() for l in file.readlines()], algorithm)

    return image


if __name__ == '__main__':
    with open("puzzle_1_input.text", "r") as f:
        image = parse_enhanceable_image(f)
        print(image)
        image.enhance()
        image.enhance()

        print(f"Lit pixels after 2x enhancement: {image.lit_pixels}")

        # enhance 48 more times
        for n in range(3, 51):
            print(f"ENHANCE! (x{n})")
            image.enhance()

        print(f"Lit pixels after 50x enhancement: {image.lit_pixels}")