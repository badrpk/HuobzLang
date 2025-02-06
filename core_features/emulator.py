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

        # Identify the opcode
        if instruction.startswith("111001"):  # VECTOR_ADD
            operands = instruction[6:]
            print(f"🛠 DEBUG: Processing VECTOR_ADD with operands {operands}")

            # Ensure we have enough operands
            if len(operands) < 6:
                print("⚠️ ERROR: VECTOR_ADD requires three valid register operands.")
                return

            src1 = operands[:2]
            src2 = operands[2:4]
            dest = operands[4:6]
            vector_add(dest, src1, src2)
            pc += 1
            continue  # Skip the rest of the loop for GPU instruction

        # Handle 4-bit opcodes (regular instructions)
        opcode = instruction[:4]
        operands = instruction[4:]
        print(f"🛠 DEBUG: Processing {opcode} with operands {operands}")

        if opcode == "0000":  # LOAD
            reg = operands[:2]
            value_part = operands[2:]
            load(reg, int(value_part, 2))
        elif opcode == "0010":  # ADD
            add(operands[:2], operands[2:4], operands[4:6])
        elif opcode == "0001":  # PRINT
            print_reg(operands[:2])
        elif opcode == "1110":  # HALT
            halt()
            break
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
