import io
from unittest import TestCase
from .main import *


class TestSubCommands(TestCase):

    @staticmethod
    def parse_input(input_str):
        with io.StringIO(input_str) as f:
            return parse_program(f)

    def test_find_biggest(self):
        # Bad answer: 92791949489795 (too low)
        # Guess 2:    92793949489995 (correct!)
        alu = ALU()
        # C = D - 2
        # G = H - 5
        # J = K - 1
        # F = I - 4
        #
        # div 26  : "........I.KLMN
        # times 26: ".B..EF...J....
        # Changes#: "AB..EF...J....
        # Branches: "...D...HI.KLMN"
        #           "ABCDEFGHIJKLMN"
        input_str = "92793949489995"
        print(check_model_number(input_str))
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            alu.run_program(refactored_program, input_str)
            self.assertEqual(0, alu.z)


    def test_find_smallest(self):
        alu = ALU()
        # C = D - 2
        # G = H - 5
        # J = K - 1
        # F = I - 4
        #
        # div 26  : "........I.KLMN
        # times 26: ".B..EF...J....
        # Changes#: "AB..EF...J....
        # Branches: "...D...HI.KLMN"
        #           "ABCDEFGHIJKLMN"
        input_str = "51131616112781"  # correct!
        print(check_model_number(input_str))
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            alu.run_program(refactored_program, input_str)
            self.assertEqual(0, alu.z)

    def test_phase_1_refactor(self):
        alu = ALU()
        inputs = [str(i) + "9999999999999" for i in range(1, 10)]

        python_outputs = [check_model_number(i) for i in inputs]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 1!")
        self.assertEqual(original_outputs, python_outputs, "Problem in python code phase 1!")

    def test_phase_2_refactor(self):
        alu = ALU()
        inputs = ["9" + str(i) + "999999999999" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 2!")

    def test_phase_3_refactor(self):
        alu = ALU()
        inputs = ["99" + str(i) + "99999999999" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 3!")

    def test_phase_4_refactor(self):
        alu = ALU()
        inputs = ["111" + str(i) + "9999999999" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 4!")

    def test_phase_5_refactor(self):
        alu = ALU()
        inputs = ["7777" + str(i) + "999999999" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 5!")

    def test_phase_6_refactor(self):
        alu = ALU()
        inputs = ["77799" + str(i) + "99999999" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 6!")

    def test_phase_7_refactor(self):
        alu = ALU()
        inputs = ["777999" + str(i) + "9999999" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 7!")

    def test_phase_8_refactor(self):
        alu = ALU()
        inputs = ["7779994" + str(i) + "999999" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 8!")

    def test_phase_9_refactor(self):
        alu = ALU()
        inputs = ["777999949" + str(i) + "99999" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 9!")

    def test_phase_10_refactor(self):
        alu = ALU()
        inputs = ["7779999499" + str(i) + "9999" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 10!")

    def test_phase_11_refactor(self):
        alu = ALU()
        inputs = ["77799994956" + str(i) + "999" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 11!")

    def test_phase_12_refactor(self):
        alu = ALU()
        inputs = ["999999999995" + str(i) + "99" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 12!")

    def test_phase_13_refactor(self):
        alu = ALU()
        inputs = ["9999999999995" + str(i) + "9" for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 13!")

    def test_phase_14_refactor(self):
        alu = ALU()
        inputs = ["5555555555555" + str(i) for i in range(1, 10)]

        with open("24/monad_program.text", "r") as f:
            program = parse_program(f)
            original_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(program, i)
                original_outputs.append(alu.z)
        with open("24/monad_program_REFACTORED.text", "r") as f:
            refactored_program = parse_program(f)
            refactor_outputs = []
            for i in inputs:
                alu.reset()
                alu.run_program(refactored_program, i)
                refactor_outputs.append(alu.z)
        self.assertEqual(original_outputs, refactor_outputs, "Problem in refactor at phase 14!")

    def test_inp(self):
        program = """inp w
        inp x
        inp y
        inp z
        inp y"""
        input_str = "12345"
        alu = ALU()
        alu.run_program(self.parse_input(program), input_str)
        self.assertEqual(alu.w, 1)
        self.assertEqual(alu.x, 2)
        self.assertEqual(alu.y, 5)
        self.assertEqual(alu.z, 4)

    def test_add(self):
        program = """add x 2
        add y 6
        add w x
        add w y"""
        alu = ALU()
        alu.run_program(self.parse_input(program))
        self.assertEqual(alu.x, 2)
        self.assertEqual(alu.y, 6)
        self.assertEqual(alu.w, 8)

    def test_mul(self):
        program = """inp x
        inp y
        mul y 2
        mul x y"""
        input_str = "22"
        alu = ALU()
        alu.run_program(self.parse_input(program), input_str)
        self.assertEqual(alu.y, 4)
        self.assertEqual(alu.x, 8)

    def test_div(self):
        program = """inp x
        add y x
        add y 2
        div y x
        div x 2"""
        input_str = "5"
        alu = ALU()
        alu.run_program(self.parse_input(program), input_str)
        self.assertEqual(alu.y, 1)
        self.assertEqual(alu.x, 2)

    def test_mod(self):
        program = """inp x
        inp y
        mod x 4
        mod y x"""
        input_str = "78"
        alu = ALU()
        alu.run_program(self.parse_input(program), input_str)
        self.assertEqual(alu.x, 3)
        self.assertEqual(alu.y, 2)

    def test_eql(self):
        program = """inp x
        inp y
        inp z
        eql x y
        eql z 4"""
        input_str = "124"
        alu = ALU()
        alu.run_program(self.parse_input(program), input_str)
        self.assertEqual(alu.x, 0)
        self.assertEqual(alu.z, 1)
