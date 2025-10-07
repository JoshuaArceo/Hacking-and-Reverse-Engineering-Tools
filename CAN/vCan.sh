#!/bin/bash

# Starts a virtual CAN interface (vcan0) for testing purposes

if [ "$#" -ne 1 ]; then
    dev = "vcan0"
else
    dev="$1"
fi


# Load the vcan module if not already loaded
if ! lsmod | grep -q vcan; then
    echo "Loading vcan module..."
    sudo modprobe vcan
fi


# Create the vcan interface if it doesn't exist
if ! ip link show "$dev" &> /dev/null; then
    echo "Creating vcan interface $dev..."
    sudo ip link add dev "$dev" type vcan
fi

# Bring the interface up
echo "Bringing up interface $dev..."
sudo ip link set "$dev" up
echo "vcan interface $dev is up and running."
ip -details link show "$dev"
echo "You can now use $dev for CAN communication."
