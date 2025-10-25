import serial.tools.list_ports
import time


useSerial = False

if useSerial:
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial('COM3', 115200)
    time.sleep(1)

while True:
    if useSerial:
        serialInst.read()