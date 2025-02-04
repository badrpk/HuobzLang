class HuobzEmulator:
    def __init__(self):
        self.registers = [0] * 16  # 16 general-purpose registers
        self.memory = [0] * 65536  # 64K memory space
        self.pc = 0  # Program counter

    def load_program(self, program):
        """Loads a program into memory."""
        self.memory[: len(program)] = program

    def execute_instruction(self, instruction):
        """Decodes and executes a single instruction."""
        if isinstance(instruction, int):  # Ensure instruction is an integer
            instruction = f"{instruction:016b}"  # Convert to 16-bit binary string

        opcode = instruction[:4]  # Extract 4-bit opcode
        reg1_bin = instruction[4:8]  # Extract first 4-bit register
        reg2_bin = instruction[8:12]  # Extract second 4-bit register
        imm_bin = instruction[8:]  # Extract 8-bit immediate value

        def get_register(value):
            """Ensures the register index is within valid range (0-15)."""
            reg = int(value, 2)
            if reg < 0 or reg >= len(self.registers):
                raise IndexError(f"Invalid register index {reg}")
            return reg

        def get_immediate(value):
            """Extracts an immediate value from 8-bit binary."""
            return int(value, 2)

        if opcode == "0001":  # LOAD Immediate
            reg = get_register(reg1_bin)
            value = get_immediate(imm_bin)
            self.registers[reg] = value
            print(f"LOAD: R{reg} = {value}")

        elif opcode == "0010":  # STORE
            reg = get_register(reg1_bin)
            address = get_immediate(imm_bin)
            if 0 <= address < len(self.memory):
                self.memory[address] = self.registers[reg]
                print(f"STORE: Mem[{address}] = R{reg} ({self.registers[reg]})")
            else:
                raise IndexError(f"Invalid memory address {address}")

        elif opcode == "0011":  # ADD
            reg1 = get_register(reg1_bin)
            reg2 = get_register(reg2_bin)
            self.registers[reg1] += self.registers[reg2]
            print(f"ADD: R{reg1} += R{reg2} ({self.registers[reg1]})")

        elif opcode == "0100":  # SUB
            reg1 = get_register(reg1_bin)
            reg2 = get_register(reg2_bin)
            self.registers[reg1] -= self.registers[reg2]
            print(f"SUB: R{reg1} -= R{reg2} ({self.registers[reg1]})")

        elif opcode == "0101":  # MUL
            reg1 = get_register(reg1_bin)
            reg2 = get_register(reg2_bin)
            self.registers[reg1] *= self.registers[reg2]
            print(f"MUL: R{reg1} *= R{reg2} ({self.registers[reg1]})")

        elif opcode == "0110":  # DIV
            reg1 = get_register(reg1_bin)
            reg2 = get_register(reg2_bin)
            if self.registers[reg2] != 0:
                self.registers[reg1] //= self.registers[reg2]
                print(f"DIV: R{reg1} /= R{reg2} ({self.registers[reg1]})")
            else:
                print(f"ERROR: Division by zero in R{reg1}.")

        elif opcode == "1000":  # JMP (Jump)
            address = get_immediate(imm_bin)
            if 0 <= address < len(self.memory):
                self.pc = address - 1  # Adjust PC since it auto-increments
                print(f"JMP: Jumping to {address}")

        elif opcode == "1010":  # JMPZ (Jump if Zero)
            reg = get_register(reg1_bin)
            address = get_immediate(imm_bin)
            if self.registers[reg] == 0:
                self.pc = address - 1
                print(f"JMPZ: Jumping to {address} because R{reg} = 0")

        elif opcode == "1011":  # JPNZ (Jump if Not Zero)
            reg = get_register(reg1_bin)
            address = get_immediate(imm_bin)
            if self.registers[reg] != 0:
                self.pc = address - 1
                print(f"JPNZ: Jumping to {address} because R{reg} != 0")

        elif opcode == "1111":  # HALT
            print("DEBUG: Execution Terminated.")
            return False  # Halt execution

        else:
            print(f"ERROR: Unrecognized opcode {opcode}. Halting execution.")
            return False  # Halt execution

        return True  # Continue execution

    def run(self):
        """Runs the loaded program."""
        while self.pc < len(self.memory):
            instruction = self.memory[self.pc]
            self.pc += 1
            if not self.execute_instruction(instruction):
                break  # Stop execution if HALT or error occurs


# Example Test
if __name__ == "__main__":
    emulator = HuobzEmulator()
    test_program = [
        0b0001000100001010,  # LOAD R1, 10
        0b0001001000000001,  # LOAD R2, 1
        0b0011000100100011,  # ADD R1, R2 (R1 = R1 + R2)
        0b0100000100100011,  # SUB R1, R2 (R1 = R1 - R2)
        0b0101000100100011,  # MUL R1, R2 (R1 = R1 * R2)
        0b0110000100100011,  # DIV R1, R2 (R1 = R1 / R2)
        0b1010000100000010,  # JMPZ R1, 2 (Jump if R1 == 0)
        0b1011001000000010,  # JPNZ R2, 2 (Jump if R2 != 0)
        0b1111000000000000,  # HALT
    ]
    emulator.load_program(test_program)
    emulator.run()
