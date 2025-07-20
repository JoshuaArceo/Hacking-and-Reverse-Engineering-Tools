import re
import serial
import time
from pathlib import Path

port = "/dev/ttyACM0"
baud = 115200
start_addr = 0x00400000
length = 0x001000
chunk_size = 0x100
line_size = 0x10
dump_file = "dump.txt"

# ChatGPT RegEx of what a valid line should look like
line_re = re.compile(r"^\[(?P<addr>[0-9A-Fa-f]{8})\]\s+((?:[0-9A-Fa-f]{8}\s+){2})-\s+((?:[0-9A-Fa-f]{8}\s+){2})(\s+.+)?$")


def read_line_from_serial(ser, expected_addr):
    for _ in range(5):  # Retry up to 5 times
        ser.reset_input_buffer()
        ser.write((f"D 0x{expected_addr:08X}\r\n").encode())

        time.sleep(0.2)

        for _ in range(20):  # Read multiple lines, find the one we care about
            line = ser.readline().decode(errors="ignore").strip()
            if f"[{expected_addr:08X}]" in line and line_re.match(line):
                return line
    raise RuntimeError(f"Failed to retrieve valid line for address 0x{expected_addr:08X}")

def main():
    # Load the current dump file
    with open(dump_file, "r") as f:
        lines = f.readlines()

    line_map = {}  
    for line in lines:
        match = line_re.match(line.strip())
        if match:
            addr = int(match.group("addr"), 16)
            line_map[addr] = line.strip()

    expected_addrs = list(range(start_addr, start_addr + length, line_size))

    ser = serial.Serial(port, baud, timeout=1)
    time.sleep(1)

    # Reconstruct the full fixed dump
    corrected_lines = []
    for addr in expected_addrs:
        if addr not in line_map or not line_re.match(line_map.get(addr, "")):
            print(f"Fixing missing/corrupt line at 0x{addr:08X}")
            try:
                line = read_line_from_serial(ser, addr)
                line_map[addr] = line
            except Exception as e:
                print(f"Error: {e}")
                continue
        corrected_lines.append(line_map[addr] + "\n")

    ser.close()

    # Backup old file
    Path(dump_file).rename(dump_file + ".bak")

    # Write the corrected dump
    with open(dump_file, "w") as f:
        f.writelines(corrected_lines)

    print(f"Dump recovery complete. Fixed file saved as: {dump_file}")

if __name__ == "__main__":
    main()

