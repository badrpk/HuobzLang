import sys
from core_features.instruction_set import INSTRUCTION_SET

def text_to_binary(text):
    """Converts a string into binary ASCII representation."""
    return " ".join(format(ord(char), "08b") for char in text)

def compile_huobzlang(source_file, output_file):
    compiled_lines = []
    labels = {}

    try:
        with open(source_file, "r") as file:
            lines = file.readlines()

        # First pass: Identify labels
        instruction_counter = 0
        for line in lines:
            line = line.strip()
            if line.endswith(":"):  # Label definition
                labels[line[:-1]] = instruction_counter
            else:
                instruction_counter += 1

        # Second pass: Compile instructions
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or line.endswith(":"):
                continue

            parts = line.split()
            instruction = parts[0].upper()

            if instruction in INSTRUCTION_SET:
                opcode = INSTRUCTION_SET[instruction]
                operands = ""

                # Handle PRINT instructions with text
                if instruction == "PRINT" and len(parts) > 1:
                    operands = text_to_binary(" ".join(parts[1:]))

                # Handle JUMP and CALL (Functions/Kernels)
                elif instruction in ["JUMP", "JUMP_IF_ZERO", "JUMP_IF_NOT_ZERO", "CALL"]:
                    label_name = parts[1]
                    if label_name in labels:
                        operands = format(labels[label_name], "012b")
                    else:
                        print(f"⚠️ Error: Label {label_name} not found!")
                        sys.exit(1)

                # Handle registers and numeric values
                elif len(parts) > 1:
                    if parts[1] in labels:
                        operands = format(labels[parts[1]], "012b")
                    elif parts[1].isdigit():
                        operands = format(int(parts[1]), "012b")
                    else:
                        print(f"⚠️ Error: Unknown reference {parts[1]}")
                        sys.exit(1)

                compiled_lines.append(f"{opcode}{operands}")

            else:
                print(f"⚠️ Unknown instruction: {instruction} - Skipping")

        # Write compiled machine code to file
        with open(output_file, "w") as out_file:
            out_file.write("\n".join(compiled_lines) + "\n")

        print(f"✅ Compilation successful: {output_file}")

    except FileNotFoundError:
        print(f"❌ Error: Source file {source_file} not found.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 core_features/compiler.py <source.hl> <output.mc>")
        sys.exit(1)

    source_file = sys.argv[1]
    output_file = sys.argv[2]
    compile_huobzlang(source_file, output_file)
