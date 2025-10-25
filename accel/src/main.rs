#![no_std]
#![no_main]

mod mpu6050;

use panic_halt as _;
use arduino_hal::{delay_ms, i2c::I2c, prelude::_unwrap_infallible_UnwrapInfallible};
use ufmt_float::uFmt_f32;

use crate::mpu6050::Mpu6050;

const MPU_ADDR: u8 = 0x68;

#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);
    let mut serial = arduino_hal::default_serial!(dp, pins, 115200);

    /*
     * For examples (and inspiration), head to
     *
     *     https://github.com/Rahix/avr-hal/tree/main/examples
     *
     * NOTE: Not all examples were ported to all boards!  There is a good chance though, that code
     * for a different board can be adapted for yours.  The Arduino Uno currently has the most
     * examples available.
     */

    let mut led = pins.d13.into_output();
    let button = pins.d2.into_pull_up_input();
    let i2c = I2c::new(
        dp.TWI,
        pins.a4.into_pull_up_input(),
        pins.a5.into_pull_up_input(),
        400000,
    );

    ufmt::uwriteln!(&mut serial, "connecting,,,").unwrap_infallible();
    let mut mpu = match Mpu6050::new(i2c, MPU_ADDR) {
        Ok(mpu) => mpu,
        Err(err) => {
            ufmt::uwriteln!(&mut serial, "{:?}", err).unwrap_infallible();
            panic!();
        }
    };
    ufmt::uwriteln!(&mut serial, "connected").unwrap_infallible();

    delay_ms(5000);
    ufmt::uwrite!(&mut serial, "Calibrating, hold the IMU level.").unwrap_infallible();
    delay_ms(2000);
    ufmt::uwrite!(&mut serial, ".").unwrap_infallible();
    delay_ms(2000);
    ufmt::uwriteln!(&mut serial, ".").unwrap_infallible();

    let mut ax = 0.;
    let mut ay = 0.;
    let mut az = 0.;
    let mut gx = 0.;
    let mut gy = 0.;
    let mut gz = 0.;
    for _ in 0..100 {
        if let Ok(data) = mpu.update() {
            ax += data.accel_x;
            ay += data.accel_y;
            az += data.accel_z;
            gx += data.gyro_x;
            gy += data.gyro_y;
            gz += data.gyro_z;
            delay_ms(10);
        }
    }

    let gains = mpu.calibration();
    gains.accel_bias[0] += ax / 100.0;
    gains.accel_bias[1] += ay / 100.0;
    gains.accel_bias[2] += az / 100.0;
    gains.gyro_bias[0] += gx / 100.0;
    gains.gyro_bias[1] += gy / 100.0;
    gains.gyro_bias[2] += gz / 100.0;

    let axg = uFmt_f32::Two(gains.accel_bias[0]);
    let ayg = uFmt_f32::Two(gains.accel_bias[1]);
    let azg = uFmt_f32::Two(gains.accel_bias[2]);
    let gxg = uFmt_f32::Two(gains.gyro_bias[0]);
    let gyg = uFmt_f32::Two(gains.gyro_bias[1]);
    let gzg = uFmt_f32::Two(gains.gyro_bias[2]);

    ufmt::uwriteln!(&mut serial, "Calibrated!").unwrap_infallible();
    ufmt::uwriteln!(&mut serial, "Accel biases X/Y/Z: {}/{}/{}", axg, ayg, azg).unwrap_infallible();
    ufmt::uwriteln!(&mut serial, "Gyro biases X/Y/Z: {}/{}/{}", gxg, gyg, gzg).unwrap_infallible();

    ufmt::uwriteln!(&mut serial, "Connected!").unwrap_infallible();

    let mut prev = button.is_low();
    loop {
        if let Ok(data) = mpu.update() {
            let new = button.is_low();
            let event = match (prev, new) {
                (false, false) => 0,
                (true, true) => 1,
                (false, true) => 2,
                (true, false) => 3,
            };
            prev = new;

            let ax = uFmt_f32::Three(data.accel_x);
            let ay = uFmt_f32::Three(data.accel_y);
            let az = uFmt_f32::Three(data.accel_z);
            let gx = uFmt_f32::Three(data.gyro_x);
            let gy = uFmt_f32::Three(data.gyro_y);
            let gz = uFmt_f32::Three(data.gyro_z);
            let temp = uFmt_f32::Two(data.temp);
            ufmt::uwriteln!(&mut serial, "{} {} {} {} {} {} {}", event, ax, ay, az, gx, gy, gz).unwrap_infallible();

            delay_ms(50);
        }
    }
}
