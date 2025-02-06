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

def sub(dest, src1, src2):
    """SUB instruction: Subtract values of two registers and store in a third register."""
    registers[dest] = registers[src1] - registers[src2]
    print(f"➖ {dest} = {registers[src1]} - {registers[src2]} → {registers[dest]}")

def mov(dest, value):
    """MOV instruction: Move a value into a register."""
    registers[dest] = value
    print(f"📤 {dest} ← {value}")

def mul(dest, src1, src2):
    """MUL instruction: Multiply values of two registers and store in a third register."""
    registers[dest] = registers[src1] * registers[src2]
    print(f"✖️ {dest} = {registers[src1]} * {registers[src2]} → {registers[dest]}")

def div(dest, src1, src2):
    """DIV instruction: Divide values of two registers and store in a third register."""
    if registers[src2] == 0:
        print("⚠️ ERROR: Division by zero")
        return
    registers[dest] = registers[src1] // registers[src2]
    print(f"➗ {dest} = {registers[src1]} / {registers[src2]} → {registers[dest]}")

def cmp(src1, src2):
    """CMP instruction: Compare two registers."""
    if registers[src1] == registers[src2]:
        print("🔍 CMP: Registers are equal.")
    elif registers[src1] < registers[src2]:
        print("🔍 CMP: Register1 is less than Register2.")
    else:
        print("🔍 CMP: Register1 is greater than Register2.")

def print_reg(reg):
    """PRINT instruction: Output the value stored in a register."""
    print(f"💡 Output: {registers[reg]}")

def halt():
    """HALT instruction: Stop execution."""
    print("🛑 HALT encountered - Stopping execution")

def vector_add(dest, src1, src2):
    """VECTOR_ADD: Perform parallel addition on vector elements."""
    print(f"🛠 DEBUG: Attempting VECTOR_ADD with src1={src1}, src2={src2}, dest={dest}")

    # Ensure registers exist
    if src1 not in registers or src2 not in registers:
        print(f"⚠️ ERROR: VECTOR_ADD invalid registers: {src1}, {src2}")
        return

    # Ensure registers contain lists (vectors)
    if not isinstance(registers[src1], list):
        print(f"⚠️ WARNING: Register {src1} does not contain a vector. Initializing to [0, 0, 0, 0]")
        registers[src1] = [0, 0, 0, 0]  # Initialize as zero vector

    if not isinstance(registers[src2], list):
        print(f"⚠️ WARNING: Register {src2} does not contain a vector. Initializing to [0, 0, 0, 0]")
        registers[src2] = [0, 0, 0, 0]  # Initialize as zero vector

    # Perform vector addition
    registers[dest] = [a + b for a, b in zip(registers[src1], registers[src2])]
    print(f"⚡ GPU VECTOR_ADD {src1} + {src2} → {dest}: {registers[dest]}")

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
        elif opcode == "0011":  # SUB
            sub(operands[:2], operands[2:4], operands[4:])
        elif opcode == "0100":  # MOV
            mov(operands[:2], int(operands[2:], 2))
        elif opcode == "0110":  # MUL
            mul(operands[:2], operands[2:4], operands[4:])
        elif opcode == "0111":  # DIV
            div(operands[:2], operands[2:4], operands[4:])
        elif opcode == "1000":  # CMP
            cmp(operands[:2], operands[2:4])
        elif opcode == "0001":  # PRINT
            print_reg(operands[:2])
        elif opcode == "1110":  # HALT
            halt()
            break
        elif opcode == "1100":  # GPU KERNEL CALL
            print(f"⚡ Executing GPU Kernel")
        elif opcode == "111001":  # VECTOR_ADD
            print(f"🛠 DEBUG: Processing VECTOR_ADD with operands {operands}")

            # Ensure we have enough operands
            if len(operands) < 6:
                print("⚠️ ERROR: VECTOR_ADD requires three valid register operands.")
                return

            src1, src2, dest = operands[:2], operands[2:4], operands[4:6]
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
