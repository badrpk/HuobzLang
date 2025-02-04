import unittest
import sys
import os

# Ensure HuobzLang modules are accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_features.emulator import HuobzEmulator


class TestEmulator(unittest.TestCase):

    def setUp(self):
        """Initialize a fresh emulator before each test."""
        self.emulator = HuobzEmulator()

    def test_load_instruction(self):
        """Test if the LOAD instruction correctly loads values into registers."""
        self.emulator.memory = ["0001000100000010"]  # LOAD R1, 2
        self.emulator.run()
        self.assertEqual(self.emulator.registers[1], 2)

    def test_add_instruction(self):
        """Test if the ADD instruction performs correct addition."""
        self.emulator.memory = [
            "0001000100000010",  # LOAD R1, 2
            "0001001000000011",  # LOAD R2, 3
            "0011000100100011"   # ADD R1, R2 -> R3 (expected: 5)
        ]
        self.emulator.run()
        self.assertEqual(self.emulator.registers[3], 5)

    def test_sub_instruction(self):
        """Test if the SUB instruction performs correct subtraction."""
        self.emulator.memory = [
            "0001000100000011",  # LOAD R1, 3
            "0001001000000010",  # LOAD R2, 2
            "0011000100100011"   # SUB R1, R2 -> R3 (expected: 1)
        ]
        self.emulator.run()
        self.assertEqual(self.emulator.registers[3], 1)

    def test_mul_instruction(self):
        """Test if the MUL instruction performs correct multiplication."""
        self.emulator.memory = [
            "0001000100000010",  # LOAD R1, 2
            "0001001000000011",  # LOAD R2, 3
            "0100000100100011"   # MUL R1, R2 -> R3 (expected: 6)
        ]
        self.emulator.run()
        self.assertEqual(self.emulator.registers[3], 6)

    def test_div_instruction(self):
        """Test if the DIV instruction performs correct division."""
        self.emulator.memory = [
            "0001000100000110",  # LOAD R1, 6
            "0001001000000011",  # LOAD R2, 3
            "0101000100100011"   # DIV R1, R2 -> R3 (expected: 2)
        ]
        self.emulator.run()
        self.assertEqual(self.emulator.registers[3], 2)

    def test_jump_instruction(self):
        """Test if the JUMP instruction correctly alters the PC."""
        self.emulator.memory = [
            "1000000000000010",  # JUMP to address 2
            "0001000100001010",  # LOAD R1, 10 (should be skipped)
            "0001001000000001"   # LOAD R2, 1 (expected execution)
        ]
        self.emulator.run()
        self.assertEqual(self.emulator.registers[2], 1)  # Only R2 should be updated

    def test_jump_if_zero_instruction(self):
        """Test if JUMP_IF_ZERO works correctly when register is zero."""
        self.emulator.memory = [
            "0001000100000000",  # LOAD R1, 0
            "1011000100000010",  # JUMP_IF_ZERO R1 -> Jump to 2
            "0001001000000001",  # LOAD R2, 1 (should be skipped)
            "0001001100000010"   # LOAD R3, 2 (expected execution)
        ]
        self.emulator.run()
        self.assertEqual(self.emulator.registers[3], 2)

    def test_jump_if_not_zero_instruction(self):
        """Test if JUMP_IF_NOT_ZERO works correctly when register is non-zero."""
        self.emulator.memory = [
            "0001000100000001",  # LOAD R1, 1
            "1100000100000010",  # JUMP_IF_NOT_ZERO R1 -> Jump to 2
            "0001001000000001",  # LOAD R2, 1 (should be skipped)
            "0001001100000010"   # LOAD R3, 2 (expected execution)
        ]
        self.emulator.run()
        self.assertEqual(self.emulator.registers[3], 2)

    def test_store_instruction(self):
        """Test if STORE instruction correctly stores register values in memory."""
        self.emulator.memory = [
            "0001000100001010",  # LOAD R1, 10
            "0010000100000001"   # STORE R1 into memory[1]
        ]
        self.emulator.run()
        self.assertEqual(self.emulator.memory[1], "0000000000001010")  # Expected stored value


if __name__ == '__main__':
    unittest.main()
