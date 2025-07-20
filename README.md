# Hardware-Reverse-Engineering-Tools
## Repository of all my custom made tools that I use in reverse engineering

## CAN Tools
These tools are used to quickly get set up using CAN 

### [Can Init](CAN/setCan.sh)
Quickly inititialize can interfaces. Takes 2 paramaters: device and baud rate.
Example: ./setCan.sh can0 500000, will initiliaze or reinitialize can0 with a baudrate of 500000


### [Can Inject](CAN/can_inject.py)
used for primitive CAN messages that don't use checksums but may using rolling counters as safety measures. This tool must be modified for each specific purpose. 
This tool works by listening for a specific ID, once  a message has been received we will parse out the nibbles that we need (typically known values for our counter and known values that we wish to modify)
We then modify the desired values and increment or decrement the counter. Since this is meant to be used for rolling counters we need to make sure we send the expected count values before the system we are spoofing sends its next value. 
For example if our rolling counter goes from 0-4, we receive a message with count 1, we want to send 2, 3, 4, 0, 1, all before the real device sends its next count of 2. This means there are limitations due to baud rate, arbitration, etc. but if we can chatter fast enough we should be ok. YMMV

