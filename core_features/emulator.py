import sys

def load_program(file_path):
    """Load machine code from file into memory."""
    try:
        with open(file_path, "r") as file:
            program = file.readlines()
        return [line.strip() for line in program if line.strip()]
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found.")
        sys.exit(1)

def execute_program(program):
    """Execute the loaded HuobzLang machine code."""
    memory = {}
    registers = {f"R{i}": 0 for i in range(16)}  # 16 General-Purpose Registers
    pc = 0  # Program Counter

    print(f"✅ Loaded program from {sys.argv[1]} ({len(program)} instructions)")

    while pc < len(program):
        instruction = program[pc]
        opcode = instruction[:4]
        operands = instruction[4:].strip()

        print(f"🔹 Executing Instruction: {instruction}")
        print(f"🟢 Executing: OPCODE={opcode}, OPERANDS={operands}")

        # HALT: Stop Execution
        if opcode == "1110":
            print("🛑 HALT encountered - Stopping execution")
            break

        # LOAD: Load a value into a register
        elif opcode == "0000":  
            register = f"R{int(operands[:4], 2)}"
            value = int(operands[4:], 2)
            registers[register] = value
            print(f"📥 {register} ← {value}")

        # ADD: Add values in two registers and store in a third
        elif opcode == "0010":
            dest = f"R{int(operands[:4], 2)}"
            src1 = f"R{int(operands[4:8], 2)}"
            src2 = f"R{int(operands[8:], 2)}"
            registers[dest] = registers[src1] + registers[src2]
            print(f"➕ {dest} = {registers[src1]} + {registers[src2]} → {registers[dest]}")

        # PRINT: Output a register value or text
        elif opcode == "0001":
            try:
                # Check if the operand is a register reference (first 4 bits indicate register)
                if operands[:4].isdigit() and int(operands[:4], 2) < 16:
                    reg_num = int(operands[:4], 2)  # Convert first 4 bits to integer (register number)
                    reg = f"R{reg_num}"
                    if reg in registers:
                        print(f"💡 Output: {registers[reg]}")  # Print register value
                    else:
                        print(f"⚠️ Error: Register {reg} not found")
                else:
                    # Convert binary ASCII to text if it's not a register reference
                    binary_chars = operands.split()
                    text = ''.join(chr(int(char, 2)) for char in binary_chars if char)
                    print(f"💡 Output: {text}")  # Print ASCII text properly
            except ValueError:
                print(f"⚠️ Error: Invalid ASCII binary for PRINT")

        # JUMP: Move to a different instruction
        elif opcode == "0101":
            jump_address = int(operands, 2)
            print(f"🔄 Jumping to instruction {jump_address}")
            pc = jump_address
            continue  # Skip PC increment

        # JUMP_IF_NOT_ZERO: Conditional Jump
        elif opcode == "0111":
            reg = f"R{int(operands[:4], 2)}"
            jump_address = int(operands[4:], 2)
            if registers[reg] != 0:
                print(f"🔄 {reg} ≠ 0, Jumping to {jump_address}")
                pc = jump_address
                continue  # Skip PC increment

        # CALL: Function Call
        elif opcode == "1010":
            print(f"📞 CALL Function at {operands}")

        # RETURN: End Function Execution
        elif opcode == "1011":
            print("🔚 RETURN from function")

        # KERNEL: Execute GPU Function
        elif opcode == "1100":
            print("⚡ Executing GPU Kernel")

        # VECTOR_ADD: Parallel Vector Addition
        elif opcode == "111001":
            print("⚡ GPU Executing: VECTOR_ADD")

        # Unrecognized Instruction
        else:
            print(f"⚠️ Unknown instruction: {opcode}")

        pc += 1  # Move to next instruction

    print("🏁 Execution complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 core_features/emulator.py <input.mc>")
        sys.exit(1)

    program = load_program(sys.argv[1])
    execute_program(program)
