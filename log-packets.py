"""
This script is intended to be run on a server that has a lora receiver plugged in.
The script will read the received lora packets over serial and save the packet contents + a timestamp to a file.
"""

import serial
import time
import sys

# open file and write header
def setup():
    fileName = sys.argv[1]
    f = open(fileName, "x")
    f.write("Log of received LoRa packets sent over serial")
    f.close()

def format_output(s):
    s = s.replace("'", "")
    s = s.replace("b", "")
    s = s.replace("\\r\\n", "\n")
    return s

def record_packet():
    ser = serial.Serial('/dev/ttyUSB0', 115200)  # open serial port (Linux)
    # ser = serial.Serial('COM6', 115200) # open serial port (Windows)
    
    fileName = sys.argv[1]
    f = open(fileName, "a")
    
    x = ser.read_until(expected=b"\r\n")
    s = format_output(str(x))
    
    currentTime = time.monotonic()
    f.write(f"Timestamp = {str(currentTime)}; Received packet = {s}\n")
    f.close()
    ser.close()

# Main
if len(sys.argv) != 2:
    print("Please enter 1 argument (fileName)")
    sys.exit()

setup()
# Run indefinitely
#while True:
record_packet()