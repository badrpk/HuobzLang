import sys

class CPU:
    def __init__(self):
        self.registers = [0] * 8  # Example: 8 general-purpose registers
        self.pc = 0  # Program counter
        self.memory = []
        self.running = True

    def get_register(self, value):
        value = value.strip()  # Remove spaces
        if not all(c in "01" for c in value):  # Ensure it's binary
            print(f"⚠️ Invalid binary register value detected: '{value}' - Skipping instruction")
            return None  # Return None to prevent crash
        return int(value, 2)

    def execute(self, opcode, operands, memory):
        print(f"🟢 Executing: OPCODE={opcode}, OPERANDS={operands}")

        if not operands:  # Prevent empty operands
            print("⚠️ No operands provided - Skipping")
            return False

        reg = self.get_register(operands[:4])
        if reg is None:
            print(f"⚠️ Skipping invalid instruction: {operands}")
            return False

        if opcode == "1110":  # Example: HALT instruction
            print("🛑 HALT encountered - Stopping execution")
            self.running = False
            return False

        elif opcode == "0000":  # Example: LOAD instruction
            value = int(operands[4:], 2)  # Convert remaining bits to int
            self.registers[reg] = value
            print(f"📥 Loaded {value} into register {reg}")

        elif opcode == "0001":  # Example: PRINT CHAR instruction
            char_code = int(operands, 2)
            print(chr(char_code), end="")  # Print character without newline

        elif opcode == "0010":  # Example: ADD instruction
            reg1 = self.get_register(operands[4:8])
            reg2 = self.get_register(operands[8:12])
            if reg1 is not None and reg2 is not None:
                self.registers[reg] = self.registers[reg1] + self.registers[reg2]
                print(f"➕ Registers[{reg1}] + Registers[{reg2}] = {self.registers[reg]}")

        else:
            print(f"⚠️ Unknown opcode: {opcode} - Skipping")

        return True  # Continue execution

class Emulator:
    def __init__(self, filename):
        self.cpu = CPU()
        self.load_program(filename)

    def load_program(self, filename):
        try:
            with open(filename, "r") as file:
                self.cpu.memory = [line.strip() for line in file.readlines()]
            print(f"✅ Loaded program from {filename} ({len(self.cpu.memory)} instructions)")
        except FileNotFoundError:
            print(f"❌ Error: File {filename} not found")
            sys.exit(1)

    def run(self):
        while self.cpu.pc < len(self.cpu.memory) and self.cpu.running:
            instruction = self.cpu.memory[self.cpu.pc]
            self.cpu.pc += 1

            if len(instruction) < 4:  # Invalid instruction length
                print(f"⚠️ Skipping invalid instruction: {instruction}")
                continue

            opcode = instruction[:4]
            operands = instruction[4:]

            if not self.cpu.execute(opcode, operands, self.cpu.memory):
                break  # Stop execution if needed

        print("\n🏁 Execution complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 emulator.py <filename.mc>")
        sys.exit(1)

    emulator = Emulator(sys.argv[1])
    emulator.run()
