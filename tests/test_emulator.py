import unittest
from emulator import HuobzEmulator

class TestEmulator(unittest.TestCase):
    def test_load_instruction(self):
        program = ["0001000100001010", "1111"]  # LOAD R1, 10; END
        emulator = HuobzEmulator()
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.registers[1], 10)

    def test_store_instruction(self):
        program = ["0001000100001010", "0010000100000001", "1111"]  # LOAD R1, 10; STORE R1, 0x0001; END
        emulator = HuobzEmulator()
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.memory[1], 10)

    def test_add_instruction(self):
        program = ["0001000100000010", "0001001000000011", "0011000100100011", "1111"]  # LOAD R1, 2; LOAD R2, 3; ADD R1, R2, R3; END
        emulator = HuobzEmulator()
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.registers[3], 5)

    def test_sub_instruction(self):
        program = ["0001000100000011", "0001001000000010", "0100000100100011", "1111"]  # LOAD R1, 3; LOAD R2, 2; SUB R1, R2, R3; END
        emulator = HuobzEmulator()
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.registers[3], 1)

    def test_mul_instruction(self):
        program = ["0001000100000010", "0001001000000011", "0101000100100011", "1111"]  # LOAD R1, 2; LOAD R2, 3; MUL R1, R2, R3; END
        emulator = HuobzEmulator()
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.registers[3], 6)

    def test_div_instruction(self):
        program = ["0001000100000110", "0001001000000011", "0110000100100011", "1111"]  # LOAD R1, 6; LOAD R2, 3; DIV R1, R2, R3; END
        emulator = HuobzEmulator()
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.registers[3], 2)

    def test_jump_instruction(self):
        program = ["1010000000000010", "1111"]  # JMP 0x0002; END
        emulator = HuobzEmulator()
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.pc, 2)

    def test_jump_if_zero_instruction(self):
        program = ["0001000100000000", "1011000100000010", "1111"]  # LOAD R1, 0; JMPZ R1, 0x0002; END
        emulator = HuobzEmulator()
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.pc, 2)

    def test_jump_if_not_zero_instruction(self):
        program = ["0001000100000001", "1100000100000010", "1111"]  # LOAD R1, 1; JMPNZ R1, 0x0002; END
        emulator = HuobzEmulator()
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.pc, 2)

if __name__ == '__main__':
    unittest.main()
