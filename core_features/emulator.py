import sys
from core_features.instruction_set import INSTRUCTION_SET
from core_features.memory import Memory
from core_features.gpu_execution import GPUExecution

class Emulator:
    def __init__(self, filename):
        self.memory = Memory()
        self.cpu_pc = 0
        self.running = True
        self.load_program(filename)
        self.gpu = GPUExecution()

    def load_program(self, filename):
        """Loads machine code into memory."""
        try:
            with open(filename, "r") as file:
                self.memory.instructions = [line.strip() for line in file.readlines()]
            print(f"✅ Loaded program from {filename} ({len(self.memory.instructions)} instructions)")
        except FileNotFoundError:
            print(f"❌ Error: File {filename} not found")
            sys.exit(1)

    def run(self):
        """Executes instructions sequentially."""
        while self.cpu_pc < len(self.memory.instructions) and self.running:
            instruction = self.memory.instructions[self.cpu_pc].strip()
            self.cpu_pc += 1

            print(f"🔹 Executing Instruction: {instruction}")

            if len(instruction) < 4:
                print(f"⚠️ Skipping invalid instruction: {instruction}")
                continue

            opcode = instruction[:4]
            operands = instruction[4:]

            if opcode in self.gpu.supported_instructions:
                self.gpu.execute(opcode, operands)
            else:
                self.execute_cpu(opcode, operands)

    def execute_cpu(self, opcode, operands):
        """Executes CPU-based instructions"""
        print(f"🟢 Executing: OPCODE={opcode}, OPERANDS={operands}")

        if opcode == INSTRUCTION_SET["HALT"]:
            print("🛑 HALT encountered - Stopping execution")
            self.running = False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 core_features/emulator.py <filename.mc>")
        sys.exit(1)

    emulator = Emulator(sys.argv[1])
    emulator.run()
