import serial.tools.list_ports
import time
from DartboardSimulator import DartboardSimulator

useSerial = False

if useSerial:
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial('COM5', 115200)
    time.sleep(0.5)
    print("Serial Connected!")

#0 angle angle angle speed
#0 - not pressed
#1 - if pressed
#2 - just pressed
#3 - just released

dartboardSimulator = DartboardSimulator((0,0,5))

while dartboardSimulator.loop(should_throw_debug=True, should_preview_debug=True):
    if useSerial:
        data = serialInst.readline().decode('utf-8').strip()
        try:
            parsedData = list(map(float, data.strip().split()))
            print(parsedData)
        except ValueError:
            print(f'parsedData ({data}) is not a list of floats separated by spaces')
        
        if False:
            parsedButtonState = parsedData[0]
            parsedXPos, parsedYPos, parsedZPos = parsedData[1], parsedData[2], parsedData[3] 
            parsedXVel, parsedYVel, parsedZVel = parsedData[4], parsedData[5], parsedData[6] 
            dart_should_be_thrown = parsedButtonState == 3
            if dart_should_be_thrown:
                dartboardSimulator.dart_manager.throw_dart(parsedXPos, parsedYPos, parsedZPos, (parsedXVel, parsedYVel, parsedZVel))
            dartboardSimulator.draw_dart_pos_preview(parsedXPos, parsedYPos) 

serialInst.close()
print("This actually happened!")