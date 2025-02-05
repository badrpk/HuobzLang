import sys

# Registers and Memory
registers = {f"R{i}": 0 for i in range(16)}  # 16 General-Purpose Registers
memory = {}
pc = 0  # Program Counter

def load(reg, value):
    """LOAD instruction: Load a value into a register."""
    registers[reg] = value
    print(f"📥 {reg} ← {value}")

def add(dest, src1, src2):
    """ADD instruction: Add values of two registers and store in a third register."""
    registers[dest] = registers[src1] + registers[src2]
    print(f"➕ {dest} = {registers[src1]} + {registers[src2]} → {registers[dest]}")

def print_reg(reg):
    """PRINT instruction: Output the value stored in a register."""
    print(f"💡 Output: {registers[reg]}")

def halt():
    """HALT instruction: Stop execution."""
    print("🛑 HALT encountered - Stopping execution")

def vector_add(dest, src1, src2):
    """VECTOR_ADD: Perform parallel addition on vector elements."""
    if src1 in registers and src2 in registers:
        if isinstance(registers[src1], list) and isinstance(registers[src2], list):
            registers[dest] = [a + b for a, b in zip(registers[src1], registers[src2])]
            print(f"⚡ GPU VECTOR_ADD {src1} + {src2} → {dest}: {registers[dest]}")
        else:
            print(f"⚠️ ERROR: VECTOR_ADD requires vector registers. Found {type(registers[src1])} and {type(registers[src2])}")
    else:
        print(f"⚠️ ERROR: Invalid registers for VECTOR_ADD: {src1}, {src2}, {dest}")

def execute_program(program):
    """Execute the given machine code program."""
    global pc
    print(f"✅ Loaded program with {len(program)} instructions")

    while pc < len(program):
        instruction = program[pc]
        opcode = instruction[:4]  # First 4 bits = opcode
        operands = instruction[4:]  # Remaining bits = operands

        print(f"🔹 Executing Instruction: {instruction}")

        if opcode == "0000":  # LOAD
            reg, value = operands[:2], int(operands[2:], 2)
            load(reg, value)
        elif opcode == "0010":  # ADD
            add(operands[:2], operands[2:4], operands[4:])
        elif opcode == "0001":  # PRINT
            print_reg(operands[:2])
        elif opcode == "1110":  # HALT
            halt()
            break
        elif opcode == "1100":  # GPU KERNEL CALL
            print(f"⚡ Executing GPU Kernel")
        elif opcode == "111001":  # VECTOR_ADD
            src1, src2, dest = operands[:2], operands[2:4], operands[4:6]
            print(f"🛠 DEBUG: Executing VECTOR_ADD with src1={src1}, src2={src2}, dest={dest}")
            vector_add(dest, src1, src2)
        else:
            print(f"⚠️ ERROR: Unknown opcode {opcode}")

        pc += 1  # Move to the next instruction

    print("🏁 Execution complete.")

# Load and execute a HuobzLang machine code program
if len(sys.argv) < 2:
    print("❌ Error: No program file provided.")
    sys.exit(1)

program_path = sys.argv[1]

try:
    with open(program_path, "r") as f:
        program = f.read().splitlines()
    execute_program(program)
except FileNotFoundError:
    print(f"❌ Error: File {program_path} not found.")
