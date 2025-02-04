import unittest
from core_features.emulator import HuobzEmulator

class TestEmulator(unittest.TestCase):

    def test_add_instruction(self):
        emulator = HuobzEmulator()
        program = [
            0b0001000100000010,  # LOAD R1, 2
            0b0001001000000011,  # LOAD R2, 3
            0b0011000100100000,  # ADD R1, R2 (Expected R1 = 5)
            0b1111000000000000,  # HALT
        ]
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.registers[1], 5)  # ✅ FIXED

    def test_sub_instruction(self):
        emulator = HuobzEmulator()
        program = [
            0b0001000100000011,  # LOAD R1, 3
            0b0001001000000010,  # LOAD R2, 2
            0b0100000100100000,  # SUB R1, R2 (Expected R1 = 1)
            0b1111000000000000,  # HALT
        ]
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.registers[1], 1)  # ✅ FIXED

    def test_mul_instruction(self):
        emulator = HuobzEmulator()
        program = [
            0b0001000100000010,  # LOAD R1, 2
            0b0001001000000011,  # LOAD R2, 3
            0b0101000100100000,  # MUL R1, R2 (Expected R1 = 6)
            0b1111000000000000,  # HALT
        ]
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.registers[1], 6)  # ✅ FIXED

    def test_div_instruction(self):
        emulator = HuobzEmulator()
        program = [
            0b0001000100000110,  # LOAD R1, 6
            0b0001001000000011,  # LOAD R2, 3
            0b0110000100100000,  # DIV R1, R2 (Expected R1 = 2)
            0b1111000000000000,  # HALT
        ]
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.registers[1], 2)  # ✅ FIXED

    def test_store_instruction(self):
        emulator = HuobzEmulator()
        program = [
            0b0001000100001010,  # LOAD R1, 10
            0b0010000100000001,  # STORE R1 -> Mem[1]
            0b1111000000000000,  # HALT
        ]
        emulator.load_program(program)
        emulator.run()
        self.assertEqual(emulator.memory[1], 10)  # ✅ FIXED

if __name__ == '__main__':
    unittest.main()
