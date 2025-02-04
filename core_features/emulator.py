






class HuobzEmulator:
    def __init__(self):
        self.memory = [0] * 65536  # 64KB memory
        self.registers = [0] * 16  # 16 registers (R0 - R15)
        self.pc = 0  # Program Counter
        self.halted = False
        self.visited_addresses = set()  # Track visited PC addresses for loop detection

    def load_program(self, program):
        """ Load the program (list of 16-bit instructions) into memory """
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def execute_instruction(self, instruction):
        """ Decode and execute a single instruction """
        instruction = f"{instruction:016b}"  # Convert to 16-bit binary
        opcode, operands = instruction[:4], instruction[4:]

        def get_register(bits):
            """ Convert binary to register index, ensuring it's within range """
            reg = int(bits, 2)
            if 0 <= reg < len(self.registers):
                return reg
            else:
                print(f"ERROR: Invalid register index {reg}. Must be between 0-15.")
                return None

        if opcode == "0001":  # LOAD: Load immediate value into register
            reg = get_register(operands[:4])
            value = int(operands[4:], 2)
            if reg is not None:
                self.registers[reg] = value
                print(f"LOAD: R{reg} = {value}")

        elif opcode == "0010":  # STORE: Store register value into memory
            reg = get_register(operands[:4])
            address = int(operands[4:], 2)
            if reg is not None:
                self.memory[address] = self.registers[reg]
                print(f"STORE: Mem[{address}] = R{reg} ({self.registers[reg]})")

        elif opcode == "0011":  # ADD: Register addition
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if reg1 is not None and reg2 is not None:
                self.registers[reg1] += self.registers[reg2]
                print(f"ADD: R{reg1} += R{reg2} ({self.registers[reg1]})")

        elif opcode == "0100":  # SUB: Register subtraction
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if reg1 is not None and reg2 is not None:
                self.registers[reg1] -= self.registers[reg2]
                print(f"SUB: R{reg1} -= R{reg2} ({self.registers[reg1]})")

        elif opcode == "0101":  # MUL: Register multiplication
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if reg1 is not None and reg2 is not None:
                self.registers[reg1] *= self.registers[reg2]
                print(f"MUL: R{reg1} *= R{reg2} ({self.registers[reg1]})")

        elif opcode == "0110":  # DIV: Register division
            reg1 = get_register(operands[:4])
            reg2 = get_register(operands[4:])
            if reg1 is not None and reg2 is not None:
                if self.registers[reg2] != 0:
                    self.registers[reg1] //= self.registers[reg2]
                    print(f"DIV: R{reg1} /= R{reg2} ({self.registers[reg1]})")
                else:
                    print("ERROR: Division by zero. Halting execution.")
                    return False

        elif opcode == "1010":  # JMP: Unconditional jump
            jump_address = int(operands, 2)
            if jump_address in self.visited_addresses:
                print(f"ERROR: Infinite loop detected at PC {jump_address}. Halting execution.")
                return False
            self.visited_addresses.add(jump_address)
            print(f"JMP: Jumping to {jump_address}")
            self.pc = jump_address - 1  # Adjust PC

        elif opcode == "1011":  # JMPZ: Jump if Zero
            reg = get_register(operands[:4])
            jump_address = int(operands[4:], 2)
            if reg is not None and self.registers[reg] == 0:
                print(f"JMPZ: Jumping to {jump_address} because R{reg} = 0")
                self.pc = jump_address - 1

        elif opcode == "1111":  # HALT: Stop execution
            print("DEBUG: Execution Terminated.")
            self.halted = True
            return False

        else:
            print(f"ERROR: Unrecognized opcode {opcode}. Halting execution.")
            return False

        return True

    def run(self):
        """ Run the loaded program until HALT """
        while not self.halted and self.pc < len(self.memory):
            instruction = self.memory[self.pc]
            if not self.execute_instruction(instruction):
                break
            self.pc += 1  # Move to the next instruction

# Example program with fixed register indices
if __name__ == "__main__":
    program = [
        0b0001000100000010,  # LOAD R1, 2
        0b0001001000000011,  # LOAD R2, 3
        0b0101000100100000,  # MUL R1, R2
        0b0110000100100000,  # DIV R1, R2
        0b1010000000000101,  # JMP 5
        0b1111000000000000,  # HALT
    ]
    
    emulator = HuobzEmulator()
    emulator.load_program(program)
    emulator.run()
