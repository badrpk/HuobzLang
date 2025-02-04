class HuobzEmulator:
    def __init__(self):
        self.registers = [0] * 16  # 16 general-purpose registers
        self.memory = [0] * 65536   # 64K memory space
        self.pc = 0                 # Program Counter (PC)
        self.running = True         # Flag to indicate if the program is running

    def load_program(self, program):
        """Load a program into memory, ensuring all instructions are strings."""
        self.memory[:len(program)] = [str(instr) for instr in program]

    def execute_instruction(self, instruction):
        """Decode and execute a single instruction."""
        opcode = instruction[:4]
        operands = instruction[4:]

        print(f"Executing instruction: {instruction}, PC: {self.pc}")

        if opcode == "0001":  # LOAD Rn, Immediate
            reg = int(operands[:4], 2)
            value = int(operands[4:], 2)
            self.registers[reg] = value

        elif opcode == "0010":  # STORE Rn, Address
            reg = int(operands[:4], 2)
            address = int(operands[4:], 2)
            self.memory[address] = self.registers[reg]

        elif opcode == "0011":  # ADD R1, R2 -> R3
            reg1 = int(operands[:4], 2)
            reg2 = int(operands[4:8], 2)
            reg3 = int(operands[8:], 2)
            self.registers[reg3] = self.registers[reg1] + self.registers[reg2]

        elif opcode == "0100":  # SUB R1, R2 -> R3
            reg1 = int(operands[:4], 2)
            reg2 = int(operands[4:8], 2)
            reg3 = int(operands[8:], 2)
            self.registers[reg3] = self.registers[reg1] - self.registers[reg2]

        elif opcode == "1010":  # JMP (Unconditional Jump)
            address = int(operands, 2)
            print(f"DEBUG: Unconditional Jump to {address}")
            self.pc = address
            return  # Prevents extra PC increment

        elif opcode == "1011":  # JMPZ (Jump if Zero)
            reg = int(operands[:4], 2)
            address = int(operands[4:], 2)
            print(f"DEBUG: JMPZ Checking R{reg}={self.registers[reg]}, Jump to {address} if Zero")

            if self.registers[reg] == 0:
                self.pc = address  # Correct jump
            else:
                self.pc += 1  # Move to next instruction if condition fails
            return  # Ensure no double PC increment

        elif instruction[:4] == "1111":  # END (Stop Execution)
            print("DEBUG: Execution Terminated.")
            self.running = False

    def run(self):
        """Run the program loaded in memory."""
        while self.pc < len(self.memory) and self.running:
            instruction = self.memory[self.pc]

            # Ensure instruction is a string
            if isinstance(instruction, int):  
                instruction = f"{instruction:016b}"

            self.execute_instruction(instruction)

            print(f"PC: {self.pc}, Registers: {self.registers}")

            # Only increment PC if the instruction was NOT a jump
            if instruction[:4] not in ["1010", "1011", "1100"]:
                self.pc += 1


# **✅ Fixed Test Program**
program = [
    "0001000100001010",  # LOAD R1, 10
    "0010000100000001",  # STORE R1 at Address 0x0001
    "0011000100100011",  # ADD R1 + R2 -> R3
    "0100001000100011",  # SUB R1 - R2 -> R3
    "1011000100000110",  # JMPZ R1, 0x0006 (Should not jump if R1 != 0)
    "1111000000000000"   # END
]

emulator = HuobzEmulator()
emulator.load_program(program)
emulator.run()
print("Final Register Values:", emulator.registers)
