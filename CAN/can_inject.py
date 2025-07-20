#!/bin/python3

import can
import time

interface = 'can0'  # Change
listen_id = 0x091   # Set to desired ID 
def wait_and_respond(): 
    bus = can.Bus(channel=interface, bustype='socketcan')

    print("Waiting for messages on ID "+ hex(listen_id))
  
  
    while True:
        msg = bus.recv()
        if msg.arbitration_id == listen_id and len(msg.data) >= 6:
            # This specific device has 2 counters
            b3 = msg.data[3]
            b4 = msg.data[4]

            upper_b3 = (b3 & 0xF0) >> 4
            lower_b3 = b3 & 0x0F
            
            upper_b4 = (b4 & 0xF0) >> 4
            lower_b4 = b4 & 0x0F


            if 0 <= lower_b3 <= 0x0F and 0 <= lower_b4 <= 0x0F:

                for i in range(15):
                    # This counter increments
                    lower_b3 = lower_b3 + 1
                    
                    # This counter decrements
                    lower_b4 = lower_b4 - 1 

                    # Update the byte using the new nibble values
                    count_b3 = (upper_b3 << 4) | ((lower_b3) & 0x0F)
                    count_b4 = (upper_b4 << 4) | ((lower_b4) & 0x0F)

                    data = msg.data
                    # Update the data bytes with the new values
                    data[0] = 0xD0
                    data[1] = 0x80
                    # Update counter bytes
                    data[3] = count_b3
                    data[4] = count_b4

                    response = can.Message(arbitration_id=listen_id, data=data, is_extended_id=False)
                    try:
                        bus.send(response)
                    except can.CanError as e:
                        print(f"Failed to send: {e}")

                    
                    time.sleep(0.004)


if __name__ == "__main__":
    wait_and_respond()

