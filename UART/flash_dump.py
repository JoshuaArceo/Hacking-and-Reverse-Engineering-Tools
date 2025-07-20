import serial
import time

# Used to manually dump flash from an old Foscam IP Camera

port = "/dev/ttyACM0"
baud = 115200
start_addr = 0x00400000
length = 0x001000
chunk_size = 0x100
output_file = "dump.txt"

# Calling D returned 16 lines of memory 
lines_per_block = 16

# Filter out input echoing, and prompt line
# Returns true if the line should be skipped
def skip_line(line, cmd_addr):
    strip = line.strip()
    return (
        strip == f"D 0x{cmd_addr:08X}" or
        strip.startswith("Displaying memory ") or 
        strip.startswith("bootloader >") or
        strip == ""
    )


def dump_block(ser, addr):
    ser.reset_input_buffer()
    ser.write((f"D 0x{addr:08X}\r\n").encode())
    time.sleep(0.1)
    block = []
    while len(block) < lines_per_block:
        try:
            line = ser.readline().decode(errors="ignore").strip()
        except Exception:
            continue
        if not skip_line(line,addr):
            block.append(line)
    return block



def main():
    ser = serial.Serial(port, baud, timeout = 1)
    time.sleep(1)

    with open(output_file, "w") as out:
        for offset in range(0, length, chunk_size):
            addr = start_addr + offset
            print(f"Dumping block at 0x{addr:08X}")
            try:
                block = dump_block(ser, addr)
                for line in block:
                    out.write(line + "\n")
                print(f"Wrote {len(block)} lines")
            except RuntimeError as e:
                print(e)
                break
    ser.close()
    print(f"Dump coplete, output saved to {output_file}")

if __name__ == "__main__":
    main()

