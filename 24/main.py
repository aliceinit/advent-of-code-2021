class ALU:
    def __init__(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.var_names = ["w", "x", "y", "z"]

    def reset(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def run_program(self, program_instructions: list, input_str: str = ""):
        for instruction in program_instructions:
            if len(instruction) == 0:
                continue  # New ALU supports blank lines!
            i = instruction.split(" ")

            if i[0].startswith("#"):
                continue  # New ALU supports comment lines

            op = i[0]
            var_name = i[1]
            if op == "inp":
                input_str = self.inp(var_name, input_str)
            elif op == "prn":
                self.prn(var_name)
            else:
                self.__getattribute__(op)(var_name, i[2])

    def inp(self, var_name: str, input_str: str):
        # Get the first digit from the input
        i = int(input_str[0])
        self.__setattr__(var_name, i)
        return input_str[1:]

    def prn(self, var_name):
        # new ALU supports printing for debug!
        print(f"value of {var_name} = {self.__getattribute__(var_name)}")

    def add(self, var_name, val):
        if val in self.var_names:
            val = self.__getattribute__(val)
        else:
            val = int(val)
        self.__setattr__(var_name, self.__getattribute__(var_name) + val)

    def mul(self, var_name, val):
        if val in self.var_names:
            val = self.__getattribute__(val)
        else:
            val = int(val)
        self.__setattr__(var_name, self.__getattribute__(var_name) * val)

    def div(self, var_name, val):
        if val in self.var_names:
            val = self.__getattribute__(val)
        else:
            val = int(val)
        self.__setattr__(var_name, int(self.__getattribute__(var_name) / val))

    def mod(self, var_name, val):
        if val in self.var_names:
            val = self.__getattribute__(val)
        else:
            val = int(val)
        self.__setattr__(var_name, self.__getattribute__(var_name) % val)

    def eql(self, var_name, val):
        if val in self.var_names:
            val = self.__getattribute__(val)
        else:
            val = int(val)
        self.__setattr__(var_name,
                         1 if self.__getattribute__(var_name) == val else 0)


def check_model_number(model_num_str):
    model_num = [int(c) for c in model_num_str]
    progression = ""
    # Phase 1
    A = model_num[0]
    z_val = A + 8
    progression += f"{z_val} => "

    # Phase 2
    B = model_num[1]
    z_val = z_val * 26 + B + 13
    progression += f"{z_val} => "

    # Phase 3
    C = model_num[2]
    x_val = C + 2
    progression += f"{z_val} => "

    # Phase 4
    D = model_num[3]
    if x_val != D:
        print(f"D needs {x_val}")
        z_val = z_val * 26 + D + 7
    else:
        print("D Achieved")
    progression += f"{z_val} => "

    # Phase 5
    E = model_num[4]
    z_val = z_val * 26 + E + 11
    progression += f"{z_val} => "

    # Phase 6
    F = model_num[5]
    z_val = z_val * 26 + F + 4
    progression += f"{z_val} => "

    # Phase 7
    G = model_num[6]
    x_val = G + 5
    progression += f"{z_val} => "

    # Phase 8
    H = model_num[7]
    if x_val != H:
        print(f"H needs {x_val}")
        z_val = z_val * 26 + H + 13
    else:
        print("H Achieved")
    progression += f"{z_val} => "

    # Phase 9
    I = model_num[8]
    if (z_val % 26) - 9 == I:
        print("I Achieved")
        # H + 4 = I (if H != G + 5)
        # else I = F + 4
        z_val = int(z_val / 26)
    else:
        print(f"I Needs {(z_val % 26) - 9}: {z_val} => {z_val % 26} => {(z_val % 26) - 9}")
        z_val = int(z_val / 26) * 26 + I + 10
    progression += f"{z_val} => "

    # Phase 10
    J = model_num[9]
    z_val = z_val * 26 + J + 1
    progression += f"{z_val} => "

    # Phase 11
    K = model_num[10]
    if K == J + 1:
        print("K Achieved")
        z_val = int(z_val / 26)
    else:
        print(f"K Needs {J + 1}")
        z_val = int(z_val / 26) * 26 + K + 2
    progression += f"{z_val} => "

    # Phase 12
    L = model_num[11]
    if L == (z_val % 26) - 5:
        # L = K - 3 (if K != J+1)
        print("L Achieved")
        z_val = int(z_val / 26)
    else:
        print(f"L Needs {(z_val % 26) - 5}: {z_val} => {z_val % 26} => {(z_val % 26) - 5}")
        z_val = int(z_val / 26) * 26 + L + 14
    progression += f"{z_val} => "

    # Phase 13
    M = model_num[12]
    if M == (z_val % 26) - 6:
        print("M Achieved")
        # M = L + 8  (if L != K - 3)
        z_val = int(z_val / 26)
    else:
        print(f"M Needs {(z_val % 26) - 6}")
        z_val = int(z_val / 26) * 26 + M + 6
    progression += f"{z_val} => "

    # Phase 14
    N = model_num[13]
    if N == (z_val % 26) - 12:
        # N = M - 6 (if M != L+8)
        print("N Achieved")
        z_val = int(z_val / 26)
    else:
        print(f"N Needs {(z_val % 26) - 12}")
        z_val = int(z_val / 26) * 26 + N + 14
    progression += f"{z_val}"
    print(progression)
    return z_val


def parse_program(file):
    return [l.strip() for l in file.readlines()]


if __name__ == '__main__':
    with open("monad_program.text", "r") as f:
        instructions = parse_program(f)
        alu = ALU()
        model_number = None
        next_check = "99999975783566"

        # find biggest input string!
        while model_number is None:
            alu.reset()
            alu.run_program(instructions, next_check)
            print(f"Running program with input {next_check} ==> {alu.z}")
            if alu.z == 0:
                model_number = next_check
            else:
                "...991"
                "...989"
                "...988"
                "...899"
                "...898"
                "...897"
                "...891"
                "...889"
                "...811"
                "...799"
                d = next_check[-1]
                if d != "1":
                    next_check = next_check[0:-1] + str(int(d) - 1)
                else:
                    i = 13
                    while d == "1":
                        next_check = next_check[0:i] + "9" + next_check[i + 1:]
                        i -= 1
                        d = next_check[i]
                    next_check = next_check[0:i] + str(int(d) - 1) + next_check[i + 1:]
        print(f"Largest valid model number = {model_number}")
