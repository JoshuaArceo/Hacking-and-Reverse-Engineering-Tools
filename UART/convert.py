import re
from pathlib import Path

input_file = "dump.txt"
output_file = "out.bin"

line_re = re.compile(r"\[([0-9A-Fa-f]+)\]\s+((?:[0-9A-Fa-f]{8}\s+){2})-\s+((?:[0-9A-Fa-f]{8}\s+){2})")

def hex_to_bytes(hex_word):
    return bytes.fromhex(hex_word)

def main():
    with open(input_file, "r") as f, open(output_file, "wb") as out:
        for line in f:
            match = line_re.match(line)
            if not match:
                continue
            hex_parts = match.group(2).split() + match.group(3).split()
            for word in hex_parts:
                out.write(hex_to_bytes(word))

    print(f"Binary written to {output_file}")

if __name__ == "__main__":
    main()

