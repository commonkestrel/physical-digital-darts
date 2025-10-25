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
        parsedData = serialInst.read()
        parsedButtonState = 0 
        parsedXPos, parsedYPos, parsedZPos = 0, 0 , 0 #Will probably need to be scaled into pygame screen coordinates
        parsedXVel, parsedYVel, parsedZVel = 0, 0 , 0 #Will probably need to be scaled into pygame screen coordinates
        #Parse the serial data in a particular way, if button released, then throw dart
        dart_should_be_thrown = False #based on parsedButtonState
        if dart_should_be_thrown:
            dartboardSimulator.dart_manager.throw_dart(parsedXPos, parsedYPos, parsedZPos, (parsedXVel, parsedYVel, parsedZVel))
        dartboardSimulator.draw_dart_pos_preview(parsedXPos, parsedYPos) #Will probably need to be scaled into pygame screen 