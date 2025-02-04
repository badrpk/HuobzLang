import sys

def compile_huobzlang(source_code):
    """Convert HuobzLang to binary machine code."""
    compiled_code = []
    lines = source_code.strip().split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("PRINT"):
            message = line.split("PRINT")[1].strip().strip('"')
            compiled_code.append("1110000000000000")  # PRINT opcode
            for char in message:
                compiled_code.append(f"{ord(char):016b}")  # Convert chars to binary
        else:
            print(f"ERROR: Unrecognized command -> {line}")
            sys.exit(1)

    return compiled_code

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 compiler.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]
    output_file = source_file.replace(".hl", ".mc")

    with open(source_file, "r") as f:
        source_code = f.read()

    machine_code = compile_huobzlang(source_code)

    with open(output_file, "w") as f:
        f.write("\n".join(machine_code))

    print(f"Compilation successful: {output_file}")
