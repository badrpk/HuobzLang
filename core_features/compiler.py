import sys

# Define a basic instruction set
INSTRUCTION_SET = {
    "HALT": "1110",  # Stop execution
    "LOAD": "0000",  # Load value into register
    "PRINT": "0001",  # Print ASCII character
    "ADD": "0010"  # Example: Add two registers
}

def text_to_binary(text):
    """Converts a text string to binary (ASCII representation)."""
    return " ".join(format(ord(char), "08b") for char in text)

def compile_huobzlang(source_file, output_file):
    compiled_lines = []

    try:
        with open(source_file, "r") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()

            # Skip empty lines or comments (lines starting with #)
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if not parts:
                continue

            instruction = parts[0].upper()

            if instruction in INSTRUCTION_SET:
                opcode = INSTRUCTION_SET[instruction]
                operands = ""

                # Handle special instructions
                if instruction == "PRINT" and len(parts) > 1:
                    operands = text_to_binary(" ".join(parts[1:]))  # Convert text to binary

                elif len(parts) > 1:
                    operands = format(int(parts[1]), "012b")  # Convert numbers to binary

                compiled_lines.append(f"{opcode}{operands}")

            elif instruction.isnumeric():  # Direct binary instructions (ensure valid)
                if all(c in "01" for c in instruction):
                    compiled_lines.append(instruction)
                else:
                    print(f"⚠️ Warning: Invalid binary sequence skipped - {instruction}")

            else:
                print(f"⚠️ Unknown instruction: {instruction} - Skipping")

        # Write compiled binary to .mc file
        with open(output_file, "w") as out_file:
            out_file.write("\n".join(compiled_lines) + "\n")

        print(f"✅ Compilation successful: {output_file}")

    except FileNotFoundError:
        print(f"❌ Error: Source file {source_file} not found.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 compiler.py <source.hl> <output.mc>")
        sys.exit(1)

    source_file = sys.argv[1]
    output_file = sys.argv[2]
    compile_huobzlang(source_file, output_file)
