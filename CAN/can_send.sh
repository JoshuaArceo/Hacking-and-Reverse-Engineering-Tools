#!/bin/bash

# Takes two arguments, the can device and ascii text
# e.g. ./can_send.sh can0 "Hello World"
# Converts the ascii text to hex and sends it as a CAN frame
# If the text is longer than 8 bytes, it will split into multiple frames

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <can_device> <ascii_text>"
    exit 1
fi

can_dev="$1"
text="$2"
max_len=8

ascii_to_hex() {
    echo -n "$1" | xxd -p | tr -d '\n'
}

send_can_frame() {
    local id="$1"
    local data="$2"
    echo "Sending CAN frame on $can_dev: ID=$id DATA=$data"
    cansend "$can_dev" "$id#$data"
}

text_len=${#text}
if [ "$text_len" -le "$max_len" ]; then
    hex_data=$(ascii_to_hex "$text")
    send_can_frame "123" "$hex_data"
else
    for (( i=0; i<text_len; i+=max_len )); do
        chunk=${text:i:max_len}
        hex_data=$(ascii_to_hex "$chunk")
        send_can_frame "123" "$hex_data"
    done
fi
