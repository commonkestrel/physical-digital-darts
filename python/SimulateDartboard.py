import serial.tools.list_ports
import time
from DartboardSimulator import DartboardSimulator

useSerial = False
dartboardSimulator = DartboardSimulator((0,3,5))

if useSerial:
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial('COM3', 115200)
    time.sleep(1)

#0 v v v p p p
#0 - not pressed
#1 - if pressed
#2 - just pressed
#3 - just released

while dartboardSimulator.loop(should_throw_debug=True, should_preview_debug=True):
    if useSerial:
        numBytes = serialInst.in_waiting
        data = serialInst.read(numBytes)
        parsedData = list(map(int, data.strip().split()))
        parsedButtonState = parsedData[0]
        parsedXPos, parsedYPos, parsedZPos = parsedData[1], parsedData[2], parsedData[3] 
        parsedXVel, parsedYVel, parsedZVel = parsedData[4], parsedData[5], parsedData[6] 
        dart_should_be_thrown = parsedButtonState == 3
        if dart_should_be_thrown:
            dartboardSimulator.dart_manager.throw_dart(parsedXPos, parsedYPos, parsedZPos, (parsedXVel, parsedYVel, parsedZVel))
        dartboardSimulator.draw_dart_pos_preview(parsedXPos, parsedYPos) 