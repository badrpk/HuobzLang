import sys
import os

# Instruction mapping
INSTRUCTION_SET = {
    "PRINT": "0001"
}

def parse_line(line):
    """ Parse a line of HuobzLang and convert it to machine code. """
    line = line.strip()
    
    if line.startswith("PRINT "):
        message = line[6:].strip().strip('"')
        return INSTRUCTION_SET["PRINT"] + f" {message}"  # Simple encoding

    return None  # Unknown instruction

def compile_file(input_path, output_path):
    """ Compile a HuobzLang source file into machine code. """
    compiled_code = []
    
    with open(input_path, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        compiled_line = parse_line(line)
        if compiled_line:
            compiled_code.append(compiled_line)
    
    if compiled_code:
        with open(output_path, "w") as f:
            f.write("\n".join(compiled_code))
        print(f"Compilation successful: {output_path}")
    else:
        print(f"ERROR: No valid instructions in {input_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 compiler.py <source_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.replace(".hl", ".mc")  # Machine Code file

    if not os.path.exists(input_file):
        print(f"ERROR: File {input_file} does not exist.")
        sys.exit(1)

    compile_file(input_file, output_file)
