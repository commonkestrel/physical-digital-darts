# Physical Digital Darts
## 💡 Inspiration

As a team who values accessible and immersive gaming experiences, we wanted to create a hack that embodied both of these ideas across software, hardware, and design. Taking inspiration from the Nintendo Wii and Switch consoles, we choose to create a Physical Digital Dart which allows the user to perform throwing motions as they would in real life, captures that motion with an accelerometer, and simulates the result on a digital dartboard.

---

## 🎯 What It Does

After the MPU6050 accelerometer reads its current angles, those angles are filtered for noise on the Arduino Nano which then transmits the button state, roll, pitch, and yaw of the Physical Digital Dart via serial monitor to our Python dartboard simulator which launches a dart in the correct direction on the button’s release at the angle given by the MPU6050.

To account for drift, a double tap of the button re-calibrates the dart’s orientation to a standardized orientation.

---

## 🛠️ How We Built It

To optimize space and keep the dart as small as possible, we utilized small gauge wires for connections and assembled them to minimize wire overlap. The dart-like 3D printed casing contains an Arduino nano which is connected to a MPU6050 accelerometer via perfboard  Along the side of the Physical Digital Dart is one button to keep track of the start (when pressed) and end of the throw (when released).

---

## 🧱 Challenges We Ran Into

The accelerometer we were provided is an MPU6050 accelerometer and gyroscope. This type of small MEMS sensor is great for finding orientation, but velocity and position are far out of reach for the level of inaccuracy and drift found in the sensor. In order to fix this, we developed a specialized filtering algorithm for our application that was able to combat these issues and keep the drift in check. 

Additionally, as we sought to use the 3D printers on the first day of the hackathon, we found that 3/4 were malfunctioning. In order to print our design and let others print theirs we worked through the night to fix the Prusa I3 Mark 2, the Ender 3, and the Ender 3 V2 SE, ultimately getting all 3 printers into a functioning state.

---

## 🏆 Accomplishments That We're Proud Of

1. Combining software, hardware, AND 3D design into a working product with very limited time 
2. Creating a product which can be adjusted in shape to meet the needs of its users
3. Creating a product which combines the physical and digital worlds, redefining what it means to “play a game."

---

## 📚 What We Learned

For our future hackathons, we noted that it would be best to bring as much personal hardware as needed, considering that there may not be a sufficient amount of hardware available to borrow from the venue. 

---

## 🚀 What's Next for Digital Physical Darts (Wii Darts)

### 2D → 3D
Since our current version is 2D, we would like to implement a 3D version with better visuals and more character. Some additional features include:
- Player-versus-player gameplay
- A Wii Sports-like aesthetics

### Fix Accelerometer Drift
Originally, our team wanted to track the position of the dart at all times but found that the drift of the MPU6050 made the double integration necessary to find that position highly accurate. A more precise accelerometer combined with a more intense filtering algorithm such as a Kalman filter would yield better results.
