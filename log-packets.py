"""
This script is intended to be run on a server that has a lora receiver plugged in.
The script will read the received lora packets over serial and save the packet contents + a timestamp to a file.
"""

import serial
from datetime import datetime
import sys

# open file and write header
def setup():
    fileName = sys.argv[1]
    f = open(fileName, "x")
    f.write("Log of received LoRa packets sent over serial \n")
    f.close()
    # ser = serial.Serial('/dev/ttyUSB0', 115200)  # open serial port (Linux)
    ser = serial.Serial('COM3', 115200) # open serial port (Windows)
    return ser

def format_output(s):
     s = s.replace("'", "")
     s = s.replace("b", "")
     s = s.replace("\\r\\n", "")
     return s

def record_packet(ser):
    
    fileName = sys.argv[1]
    f = open(fileName, "a")
    
    x = ser.read_until(expected=b"\r\n")
    s = format_output(str(x))
    
    currentTime = datetime.now()
    dt_string = currentTime.strftime("%m/%d/%Y %H:%M:%S")
    f.write(f"Timestamp = {dt_string}; Received packet = {s}\n")
    f.close()

# Main
if len(sys.argv) != 2:
    print("Please enter 1 argument (fileName)")
    sys.exit()

ser = setup()
# Run indefinitely
while True:
    record_packet(ser)