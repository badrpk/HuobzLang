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
        registers[src1] = [0, 0, 0, 0]  # Initialize as zero vector

    if not isinstance(registers[src2], list):
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

        # DEBUG: Show current execution step
        print(f"🔹 Executing Instruction: {instruction}")
        print(f"🛠 DEBUG: Current Program Counter (PC) = {pc}")

        # Check for 5-bit opcode instructions first
        if instruction.startswith("11101"):  # VECTOR_ADD Opcode Fix
            operands = instruction[5:]
            print(f"🛠 DEBUG: Processing VECTOR_ADD with raw operands: {operands}")

            if len(operands) < 6:
                print(f"⚠️ ERROR: VECTOR_ADD requires three valid register operands. Received: {operands}")
                return

            try:
                dest = f"R{int(operands[:2], 2)}"
                src1 = f"R{int(operands[2:4], 2)}"
                src2 = f"R{int(operands[4:6], 2)}"

                print(f"🛠 DEBUG: Parsed VECTOR_ADD operands -> dest={dest}, src1={src1}, src2={src2}")

                vector_add(dest, src1, src2)
            except ValueError as e:
                print(f"⚠️ ERROR: Invalid operand format for VECTOR_ADD: {e}")
                return

            pc += 1
            continue  # Skip the rest of the loop

        # Handle 4-bit opcodes
        opcode = instruction[:4]
        operands = instruction[4:]

        if opcode == "0000":  # LOAD
            reg = f"R{int(operands[:2], 2)}"
            value = int(operands[2:], 2) if operands[2:] else 0
            load(reg, value)

        elif opcode == "0010":  # ADD
            add(f"R{int(operands[:2], 2)}", f"R{int(operands[2:4], 2)}", f"R{int(operands[4:6], 2)}")

        elif opcode == "0001":  # PRINT
            print_reg(f"R{int(operands[:2], 2)}")

        elif opcode == "1110":  # HALT
            halt()
            break

        elif opcode == "1100":  # GPU KERNEL CALL
            print("⚡ Executing GPU Kernel")
            gpu_mode = True  # Enter GPU mode for subsequent instructions

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
