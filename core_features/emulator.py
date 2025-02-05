import sys

# Registers and Memory
registers = {f"R{i}": 0 for i in range(16)}  # 16 General-Purpose Registers
memory = {}
pc = 0  # Program Counter
gpu_mode = False  # Flag to indicate GPU kernel execution mode

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
    print(f"🛠 DEBUG: Attempting VECTOR_ADD with operands {src1}, {src2}, {dest}")

    # Ensure registers exist
    if src1 not in registers or src2 not in registers or dest not in registers:
        print(f"⚠️ ERROR: VECTOR_ADD invalid registers: {src1}, {src2}, {dest}")
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
    global pc, gpu_mode
    print(f"✅ Loaded program with {len(program)} instructions")

    while pc < len(program):
        instruction = program[pc].strip()
        print(f"🔹 Executing Instruction: {instruction}")

        # Identify if this is a GPU instruction (VECTOR_ADD)
        if instruction[:5] in ["11101", "11100"]:  # VECTOR_ADD, VECTOR_MULTIPLY, etc.
            opcode = instruction[:5]  # First 5 bits for GPU instructions
            operands = instruction[5:]  # The rest are operands
        else:
            opcode = instruction[:4]  # First 4 bits for normal instructions
            operands = instruction[4:]  # The rest are operands

        print(f"🛠 DEBUG: Processing {opcode} with operands {operands}")

        # Execute based on opcode
        if opcode == "0000":  # LOAD
            reg = operands[:2]
            value_part = operands[2:]
            if gpu_mode:
                # Parse as vector: 4 elements, 8 bits each
                elements = []
                for i in range(0, 32, 8):
                    chunk = value_part[i:i+8] if i+8 <= len(value_part) else '00000000'
                    elements.append(int(chunk, 2))
                # Ensure exactly 4 elements, truncate or pad with 0 if needed
                elements = elements[:4] + [0]*(4 - len(elements[:4]))
                load(reg, elements)
            else:
                # Scalar load (default)
                value = int(value_part, 2) if value_part else 0
                load(reg, value)
        elif opcode == "0010":  # ADD
            add(operands[:2], operands[2:4], operands[4:6])
        elif opcode == "0001":  # PRINT
            print_reg(operands[:2])
        elif opcode == "1110":  # HALT
            halt()
            break
        elif opcode == "11101":  # VECTOR_ADD
            # Perform GPU operation like VECTOR_ADD
            src1 = f"R{int(operands[:2], 2)}"
            src2 = f"R{int(operands[2:4], 2)}"
            dest = f"R{int(operands[4:], 2)}"
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
