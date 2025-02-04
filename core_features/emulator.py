import sys

class HuobzEmulator:
    def __init__(self):
        self.memory = ["0000000000000000"] * 65536  # Memory (16-bit slots)
        self.pc = 0  # Program Counter
        self.output_buffer = ""  # Store output for PRINT

    def load_program(self, program_path):
        """Load binary program into memory."""
        try:
            with open(program_path, "r") as f:
                lines = f.readlines()
            self.memory[:len(lines)] = [line.strip() for line in lines]
        except FileNotFoundError:
            print(f"ERROR: File {program_path} not found.")
            sys.exit(1)

    def execute_instruction(self, instruction):
        """Decode and execute a 16-bit instruction."""
        if len(instruction) != 16:
            print(f"ERROR: Invalid instruction length -> {instruction}")
            return False

        opcode = instruction[:4]
        operand = instruction[4:]

        if opcode == "1110":  # PRINT Instruction
            char_code = int(operand, 2)
            if char_code == 0:  # PRINT end signal
                print(self.output_buffer)  # Print stored output
                self.output_buffer = ""  # Reset buffer
            else:
                self.output_buffer += chr(char_code)

        elif opcode == "1111":  # HALT Execution
            print("DEBUG: Execution Terminated.")
            return False

        else:
            print(f"ERROR: Unrecognized opcode {opcode}. Halting execution.")
            return False

        return True

    def run(self):
        """Run the emulator and execute instructions sequentially."""
        while self.pc < len(self.memory):
            instruction = self.memory[self.pc]

            if instruction == "0000000000000000":
                self.pc += 1
                continue  # Skip NO-OP

            if not self.execute_instruction(instruction):
                break

            self.pc += 1

# Run the emulator with a compiled machine code file
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 emulator.py <machine_code_file>")
        sys.exit(1)

    emulator = HuobzEmulator()
    emulator.load_program(sys.argv[1])
    emulator.run()
