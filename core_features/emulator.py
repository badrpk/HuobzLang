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
    print(f"🛠 DEBUG: Attempting VECTOR_ADD with operands {src1}, {src2}, {dest}")

    # Ensure registers exist and contain lists (vectors)
    for reg in [dest, src1, src2]:
        if reg not in registers:
            print(f"⚠️ ERROR: Invalid register: {reg}")
            return

        if not isinstance(registers[reg], list):
            print(f"⚠️ WARNING: Register {reg} does not contain a vector. Initializing to [0, 0, 0, 0]")
            registers[reg] = [0, 0, 0, 0]  # Initialize as zero vector
    
    # Get the length of the shortest vector to avoid IndexError
    vector_length = min(len(registers[src1]), len(registers[src2]), len(registers[dest]))

    # Perform vector addition up to the shortest vector length
    registers[dest] = [registers[src1][i] + registers[src2][i] for i in range(vector_length)]

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
        elif opcode == "0001":  # PRINT
            print_reg(operands[:2])
        elif opcode == "1110":  # HALT
            halt()
            break
        elif opcode == "1100":  # GPU KERNEL CALL
            print(f"⚡ Executing GPU Kernel")
        elif opcode == "111001":  # VECTOR_ADD
            print(f"🛠 DEBUG: Processing VECTOR_ADD with operands {operands}")

            if len(operands) < 6:
                print("⚠️ ERROR: VECTOR_ADD requires three valid register operands.")
                return

            src1, src2, dest = operands[:2], operands[2:4], operands[4:6]
            vector_add(dest, src1, src2)
        else:
            print(f"⚠️ ERROR: Unknown opcode {opcode}")

        pc += 1  # Move to the next instruction

    print("🏁 Execution complete.")

# ... (rest of the code for loading the program from file remains the same)

