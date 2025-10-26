import serial.tools.list_ports
import time, math
from DartboardSimulator import DartboardSimulator

useSerial = False

if useSerial:
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial('COM5', 115200)
    time.sleep(0.5)
    print("Serial Connected!")

#event roll pitch yaw velocity

#0 angle angle angle speed
#0 - not pressed
#1 - if pressed
#2 - just pressed
#3 - just released

dartboardSimulator = DartboardSimulator(5)
shot = False

while dartboardSimulator.loop(should_throw_debug=True, should_preview_debug=False):
    pass
    # if useSerial:
    #     data = serialInst.readline().decode('utf-8').strip()
    #     try:
    #         parsedData = list(map(float, data.strip().split()))
    #         #print(parsedData)
    #     except ValueError:
    #         print(f'parsedData ({data}) is not a list of floats separated by spaces')
    #         continue
        
    #     if parsedData:
    #         parsedButtonState = parsedData[0]
    #         parsedRoll, parsedPitch, parsedYaw = parsedData[2], -parsedData[1], -parsedData[3] 
    #         parsedSpeed = parsedData[4] 
    #         print(f'Angles before time of throw: Yaw: {parsedYaw}, Pitch: {parsedPitch}, Speed:{parsedSpeed}')

    #         dart_should_be_thrown = parsedButtonState == 3
    #         if dart_should_be_thrown:
    #             x_speed = math.cos(math.radians(parsedYaw))*math.sin(math.radians(parsedPitch))*parsedSpeed 
    #             y_speed = math.sin(math.radians(parsedYaw))*math.sin(math.radians(parsedPitch))*parsedSpeed
    #             z_speed = math.cos(math.radians(parsedPitch))*parsedSpeed
    #             dartboardSimulator.throw_dart([y_speed, z_speed, 1])

#serialInst.close()
print("This actually happened!")