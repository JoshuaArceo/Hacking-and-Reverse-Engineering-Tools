#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <device> <bitrate>"
    exit 1
fi

dev="$1"
baud="$2"

# Bring the interface down
echo "Bringing down interface $dev..."
sudo ip link set "$dev" down

# Set the bitrate and bring the interface up
echo "Setting up $dev with bitrate $baud..."
sudo ip link set "$dev" up type can bitrate "$baud"



