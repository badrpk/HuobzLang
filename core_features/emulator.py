class HuobzEmulator:
    def __init__(self):
        self.registers = [0] * 16  # 16 general-purpose registers
        self.memory = [0] * 65536   # 64KB memory
        self.pc = 0  # Program Counter
        self.executed_instructions = set()  # Track executed instructions to detect infinite loops

    def load_program(self, program):
        """ Load a binary program into memory """
        self.memory[:len(program)] = program

    def execute_instruction(self, instruction):
        """ Decode and execute an instruction """
        instruction = f"{instruction:016b}"  # Ensure 16-bit binary format
        opcode = instruction[:4]  # First 4 bits define the operation
        operands = instruction[4:]  # Remaining 12 bits are operands

        # Register extraction function
        def get_register(value):
            reg = int(value, 2)
            if reg < 0 or reg > 15:
                print(f"ERROR: Invalid register index {reg}. Must be between 0-15.")
                return None  # Avoid processing invalid registers
            return reg

        # ALU Operations
        if opcode == "0001":  # LOAD (R, Immediate)
            reg = get_register(operands[:4])
            value = int(operands[4:], 2)
            if reg is not None:
                self.registers[reg] = value
                print(f"LOAD: R{reg} = {value}")

        elif opcode == "0010":  # ADD (R1 = R1 + R2)
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if None not in (reg1, reg2):
                self.registers[reg1] += self.registers[reg2]
                print(f"ADD: R{reg1} += R{reg2} ({self.registers[reg1]})")

        elif opcode == "0011":  # SUB (R1 = R1 - R2)
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if None not in (reg1, reg2):
                self.registers[reg1] -= self.registers[reg2]
                print(f"SUB: R{reg1} -= R{reg2} ({self.registers[reg1]})")

        elif opcode == "0100":  # MUL (R1 = R1 * R2)
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if None not in (reg1, reg2):
                self.registers[reg1] *= self.registers[reg2]
                print(f"MUL: R{reg1} *= R{reg2} ({self.registers[reg1]})")

        elif opcode == "0101":  # DIV (R1 = R1 / R2)
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if None not in (reg1, reg2) and self.registers[reg2] != 0:
                self.registers[reg1] //= self.registers[reg2]
                print(f"DIV: R{reg1} /= R{reg2} ({self.registers[reg1]})")
            else:
                print(f"ERROR: Division by zero in R{reg2}.")

        elif opcode == "0110":  # STORE (Mem[Addr] = R)
            reg = get_register(operands[:4])
            addr = int(operands[4:], 2)
            if reg is not None:
                self.memory[addr] = self.registers[reg]
                print(f"STORE: Mem[{addr}] = R{reg} ({self.registers[reg]})")

        elif opcode == "0111":  # LOAD FROM MEMORY (R = Mem[Addr])
            reg = get_register(operands[:4])
            addr = int(operands[4:], 2)
            if reg is not None:
                self.registers[reg] = self.memory[addr]
                print(f"LOAD_MEM: R{reg} = Mem[{addr}] ({self.memory[addr]})")

        # Control Flow Operations
        elif opcode == "1000":  # JMP (Jump to address)
            target_pc = int(operands, 2)
            if 0 <= target_pc < len(self.memory):
                print(f"JMP: Jumping to {target_pc}")
                self.pc = target_pc
                return  # Skip PC increment

        elif opcode == "1001":  # JMPZ (Jump if R0 == 0)
            target_pc = int(operands, 2)
            if self.registers[0] == 0 and 0 <= target_pc < len(self.memory):
                print(f"JMPZ: Jumping to {target_pc} because R0 = 0")
                self.pc = target_pc
                return  # Skip PC increment

        elif opcode == "1010":  # JNZ (Jump if R0 != 0)
            target_pc = int(operands, 2)
            if self.registers[0] != 0 and 0 <= target_pc < len(self.memory):
                print(f"JNZ: Jumping to {target_pc} because R0 != 0")
                self.pc = target_pc
                return  # Skip PC increment

        elif opcode == "1111":  # HALT
            print("DEBUG: Execution Terminated.")
            return False  # Stop execution

        else:
            print(f"ERROR: Unrecognized opcode {opcode}. Halting execution.")
            return False  # Stop execution

        self.pc += 1  # Move to next instruction
        return True

    def run(self):
        """ Runs the program loaded into memory """
        while self.pc < len(self.memory):
            if self.pc in self.executed_instructions:
                print(f"ERROR: Infinite loop detected at PC {self.pc}. Halting execution.")
                break  # Prevent infinite loop

            self.executed_instructions.add(self.pc)

            instruction = self.memory[self.pc]
            if not self.execute_instruction(instruction):
                break

# Sample Test Program (Binary Encoded Instructions)
program = [
    0b0001000100000010,  # LOAD R1, 2
    0b0001001000000011,  # LOAD R2, 3
    0b0010000100100000,  # ADD R1, R2
    0b1000000000000101,  # JMP 5 (Infinite loop protection check)
    0b1111000000000000   # HALT
]

if __name__ == "__main__":
    emulator = HuobzEmulator()
    emulator.load_program(program)
    emulator.run()
