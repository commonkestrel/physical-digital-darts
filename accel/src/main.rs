#![no_std]
#![no_main]
#![feature(abi_avr_interrupt)]

mod mpu6050;
mod rolling_buffer;
mod f32_ufmt;

use core::cell;

use micromath::F32Ext;
use panic_halt as _;
use arduino_hal::{delay_ms, i2c::I2c, prelude::*};

use crate::{f32_ufmt::ThreeFmt, mpu6050::Mpu6050, rolling_buffer::Collection};

const IMU_ADDR: u8 = 0x68;
const ALPHA: f32 = 0.85;

#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);
    let mut serial = arduino_hal::default_serial!(dp, pins, 115200);

    millis_init(dp.TC0);

    // Enable interrupts globally
    unsafe { avr_device::interrupt::enable() };

    let button = pins.d3.into_pull_up_input();
    let i2c = I2c::new(
        dp.TWI,
        pins.a4.into_pull_up_input(),
        pins.a5.into_pull_up_input(),
        400000,
    );

    let mut imu = match Mpu6050::new(i2c, IMU_ADDR) {
        Ok(imu) => imu,
        Err(err) => {
            ufmt::uwriteln!(&mut serial, "{:?}", err).unwrap_infallible();
            panic!();
        }
    };

    ufmt::uwriteln!(&mut serial, "Connected!").unwrap_infallible();

    let init = imu.update().unwrap();
    let mut roll = (-init.accel_x).atan2((init.accel_y*init.accel_y + init.accel_z*init.accel_z).sqrt()).to_degrees();
    let mut pitch = init.accel_y.atan2(init.accel_z).to_degrees();
    let mut yaw = 0.;

    let mut vx = 0.;
    let mut prev_time = millis();
    let mut ax_gain = 0.;
    let mut gz_gain = 0.;
    let mut rolling: Collection<10> = Collection::new();
    let mut rolling_yaw: Collection<5> = Collection::new();
    let mut last_button = 0;

    let mut prev = button.is_low();
    loop {
        if let Ok(data) = imu.update() {
            let new = button.is_low();
            let event = match (prev, new) {
                (false, false) => 0,
                (true, true) => 1,
                (false, true) => 2,
                (true, false) => {
                    prev_time = millis();
                    if prev_time - last_button < 500 {
                        ax_gain = data.accel_x;
                        rolling.clear();
                        gz_gain = data.gyro_z;
                        rolling_yaw.clear();
                        roll = (-init.accel_x).atan2((init.accel_y*init.accel_y + init.accel_z*init.accel_z).sqrt()).to_degrees();
                        pitch = init.accel_y.atan2(init.accel_z).to_degrees();
                        yaw = 0.;
                        vx = 0.;
                        continue;
                    }
                    last_button = prev_time;
                    3
                },
            };
            prev = new;

            let time = millis();
            let dt = (time - prev_time) as f32 / 1000.0;

            if rolling_yaw.full() && (rolling_yaw.avg() - data.gyro_z).abs() < 0.25 {
                rolling_yaw.clear();
                gz_gain = data.gyro_z;
            } else {
                rolling_yaw.push(data.gyro_z);
            }

            roll += data.gyro_x * dt;
            pitch += data.gyro_y * dt;
            yaw += (data.gyro_z - gz_gain) * dt;
            
            // complimentary filter on our orientation :)
            let new_pitch = data.accel_y.atan2(data.accel_z).to_degrees();
            let new_roll = (-data.accel_x).atan2((data.accel_y*data.accel_y + data.accel_z*data.accel_z).sqrt()).to_degrees();

            if roll.signum() != new_pitch.signum() {
                pitch = new_pitch;
            }

            roll = ALPHA * roll + (1. - ALPHA) * new_roll;
            pitch = ALPHA * pitch + (1. - ALPHA) * new_pitch;

            if rolling.full() && (rolling.avg() - data.accel_x).abs() < 0.25 {
                rolling.clear();
                ax_gain = data.accel_x;
            } else {
                rolling.push(data.accel_x);
            }

            vx += deadband(data.accel_x - ax_gain, 1.) * dt;
            vx *= 0.5;

            prev_time = time;

            let fmtx = ThreeFmt(roll);
            let fmty = ThreeFmt(fix_pitch(pitch));
            let fmtz = ThreeFmt(yaw);
            let gx = ThreeFmt(vx.abs());
            ufmt::uwriteln!(&mut serial, "{} {} {} {} {}", event, fmtx, fmty, fmtz, gx).unwrap_infallible();

            delay_ms(50);
        }
    }
}

#[inline]
fn deadband(input: f32, band: f32) -> f32 {
    if input.abs() < band { 0. } else { input }
}

#[inline]
fn fix_pitch(pitch: f32) -> f32 {
    if pitch < 0. {
        return 180. + pitch;
    } else {
        return pitch - 180.;
    }
}

// Possible Values:
//
// ╔═══════════╦══════════════╦═══════════════════╗
// ║ PRESCALER ║ TIMER_COUNTS ║ Overflow Interval ║
// ╠═══════════╬══════════════╬═══════════════════╣
// ║        64 ║          250 ║              1 ms ║
// ║       256 ║          125 ║              2 ms ║
// ║       256 ║          250 ║              4 ms ║
// ║      1024 ║          125 ║              8 ms ║
// ║      1024 ║          250 ║             16 ms ║
// ╚═══════════╩══════════════╩═══════════════════╝
const PRESCALER: u32 = 1024;
const TIMER_COUNTS: u32 = 125;

const MILLIS_INCREMENT: u32 = PRESCALER * TIMER_COUNTS / 16000;

static MILLIS_COUNTER: avr_device::interrupt::Mutex<cell::Cell<u32>> =
    avr_device::interrupt::Mutex::new(cell::Cell::new(0));

fn millis_init(tc0: arduino_hal::pac::TC0) {
    // Configure the timer for the above interval (in CTC mode)
    // and enable its interrupt.
    tc0.tccr0a.write(|w| w.wgm0().ctc());
    tc0.ocr0a.write(|w| w.bits(TIMER_COUNTS as u8));
    tc0.tccr0b.write(|w| match PRESCALER {
        8 => w.cs0().prescale_8(),
        64 => w.cs0().prescale_64(),
        256 => w.cs0().prescale_256(),
        1024 => w.cs0().prescale_1024(),
        _ => panic!(),
    });
    tc0.timsk0.write(|w| w.ocie0a().set_bit());

    // Reset the global millisecond counter
    avr_device::interrupt::free(|cs| {
        MILLIS_COUNTER.borrow(cs).set(0);
    });
}

#[avr_device::interrupt(atmega328p)]
fn TIMER0_COMPA() {
    avr_device::interrupt::free(|cs| {
        let counter_cell = MILLIS_COUNTER.borrow(cs);
        let counter = counter_cell.get();
        counter_cell.set(counter + MILLIS_INCREMENT);
    })
}

fn millis() -> u32 {
    avr_device::interrupt::free(|cs| MILLIS_COUNTER.borrow(cs).get())
}
