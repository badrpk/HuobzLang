import sys

class HuobzEmulator:
    def __init__(self):
        self.registers = [0] * 16  # 16 general-purpose registers
        self.memory = ["0000000000000000"] * 65536  # 16-bit addressable memory
        self.pc = 0  # Program Counter
        self.executed_addresses = set()  # Track executed instructions for infinite loop detection

    def load_program(self, program):
        """Load a program (list of 16-bit binary instructions) into memory."""
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def execute_instruction(self, instruction):
        """Decode and execute a 16-bit instruction."""
        if len(instruction) != 16:
            print(f"ERROR: Invalid instruction length at PC {self.pc}. Must be 16 bits.")
            return False
        
        opcode = instruction[:4]
        operands = instruction[4:]

        def get_register(value):
            reg = int(value, 2)
            if reg < 0 or reg >= 16:
                print(f"ERROR: Invalid register index {reg}. Must be between 0-15.")
                return None
            return reg

        if opcode == "0001":  # LOAD
            reg = get_register(operands[:4])
            value = int(operands[4:], 2)
            if reg is not None:
                self.registers[reg] = value
                print(f"LOAD: R{reg} = {value}")

        elif opcode == "0010":  # STORE
            reg = get_register(operands[:4])
            addr = int(operands[4:], 2)
            if reg is not None and 0 <= addr < len(self.memory):
                self.memory[addr] = f"{self.registers[reg]:016b}"
                print(f"STORE: Mem[{addr}] = R{reg} ({self.registers[reg]})")

        elif opcode == "0011":  # ADD
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if reg1 is not None and reg2 is not None:
                self.registers[reg1] += self.registers[reg2]
                print(f"ADD: R{reg1} += R{reg2} ({self.registers[reg1]})")

        elif opcode == "0100":  # SUB
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if reg1 is not None and reg2 is not None:
                self.registers[reg1] -= self.registers[reg2]
                print(f"SUB: R{reg1} -= R{reg2} ({self.registers[reg1]})")

        elif opcode == "0101":  # MUL
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if reg1 is not None and reg2 is not None:
                self.registers[reg1] *= self.registers[reg2]
                print(f"MUL: R{reg1} *= R{reg2} ({self.registers[reg1]})")

        elif opcode == "0110":  # DIV
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if reg1 is not None and reg2 is not None:
                if self.registers[reg2] != 0:
                    self.registers[reg1] //= self.registers[reg2]
                    print(f"DIV: R{reg1} /= R{reg2} ({self.registers[reg1]})")
                else:
                    print("ERROR: Division by zero. Halting execution.")
                    return False

        elif opcode == "1000":  # JUMP
            addr = int(operands, 2)
            if 0 <= addr < len(self.memory):
                print(f"JMP: Jumping to {addr}")
                self.pc = addr - 1  # -1 to compensate for PC increment in run()
            else:
                print(f"ERROR: Invalid jump address {addr}. Halting execution.")
                return False

        elif opcode == "1001":  # JUMP IF ZERO
            reg = get_register(operands[:4])
            addr = int(operands[4:], 2)
            if reg is not None and self.registers[reg] == 0:
                print(f"JMPZ: Jumping to {addr} because R{reg} = 0")
                self.pc = addr - 1

        elif opcode == "1010":  # JUMP IF NOT ZERO
            reg = get_register(operands[:4])
            addr = int(operands[4:], 2)
            if reg is not None and self.registers[reg] != 0:
                print(f"JMPNZ: Jumping to {addr} because R{reg} ≠ 0")
                self.pc = addr - 1

        elif opcode == "1111":  # HALT
            print("DEBUG: Execution Terminated.")
            return False

        else:
            print(f"ERROR: Unrecognized opcode {opcode}. Halting execution.")
            return False

        return True

    def run(self):
        """Run the emulator, executing instructions until halted."""
        while self.pc < len(self.memory):
            if self.pc in self.executed_addresses:
                print(f"ERROR: Infinite loop detected at PC {self.pc}. Halting execution.")
                sys.exit(1)

            self.executed_addresses.add(self.pc)
            instruction = self.memory[self.pc]

            if instruction == "0000000000000000":
                print(f"DEBUG: Reached NO-OP at PC {self.pc}. Skipping.")
                self.pc += 1
                continue

            if not self.execute_instruction(instruction):
                break

            self.pc += 1

# Example test program: Load, Add, and Jump
program = [
    "0001000100000010",  # LOAD R1, 2
    "0001001000000011",  # LOAD R2, 3
    "0011000100100000",  # ADD R1, R2
    "1000000000000101",  # JMP 5
    "1111000000000000",  # HALT
]

# Run the emulator
if __name__ == "__main__":
    emulator = HuobzEmulator()
    emulator.load_program(program)
    emulator.run()
