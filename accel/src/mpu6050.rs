use arduino_hal::i2c::I2c;
use arduino_hal::{delay_ms, hal};
use embedded_hal::i2c::I2c as _;
use ufmt::derive::uDebug;

#[derive(Debug, uDebug)]
pub enum Error {
    I2c(hal::i2c::Error),
    /// Invalid byte read from the whoami register
    Identification,
    NoData,
}

impl From<hal::i2c::Error> for Error {
    fn from(value: hal::i2c::Error) -> Self {
        Self::I2c(value)
    }
}

const WHOAMI: u8 = 0x68;
const WHOAMI_REG: u8 = 0x75;
const PWR_MGMT_1: u8 = 0x6B;
const MPU_CONFIG: u8 = 0x1A;
const SMPLRT_DIV: u8 = 0x19;
const GYRO_CONFIG: u8 = 0x1B;
const INT_PIN_CFG: u8 = 0x37;
const INT_ENABLE: u8 = 0x38;
const INT_STATUS: u8 = 0x3A;
const ACCEL_XOUT_H: u8 = 0x3B;

const A_RES: f32 = 16.0 / 32768.0;
const G_RES: f32 = 2000.0 / 32768.0;

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MpuData {
    pub accel_y: f32,
    pub accel_z: f32,
    pub accel_x: f32,
    pub gyro_x: f32,
    pub gyro_y: f32,
    pub gyro_z: f32,
    pub temp: f32,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct CalData {
    pub accel_bias: [f32; 3],
    pub gyro_bias: [f32; 3],
}

impl Default for CalData {
    fn default() -> Self {
        CalData { accel_bias: [0.; 3], gyro_bias: [0.; 3] }
    }
}

pub struct Mpu6050{
    i2c: I2c,
    address: u8,
    calibration: CalData,
}

impl Mpu6050 {
    pub fn new(i2c: I2c, address: u8) -> Result<Mpu6050, Error> {
        let mut new = Mpu6050 { i2c, address, calibration: CalData::default() };
        new.init()?;

        return Ok(new)
    }

    pub fn init(&mut self) -> Result<(), Error> {
        let whoami = read_byte(&mut self.i2c, self.address, WHOAMI_REG)?;
        if whoami != WHOAMI {
            return Err(Error::Identification)
        }

        // reset device
        write_byte(&mut self.i2c, self.address, PWR_MGMT_1, 0x80)?;
        delay_ms(100);
        // wake up device
        write_byte(&mut self.i2c, self.address, PWR_MGMT_1, 0x00)?;
        delay_ms(100);

        // get stable time source
        write_byte(&mut self.i2c, self.address, PWR_MGMT_1, 0x03)?;
        delay_ms(200);

        // configure gyro and thermometer
        write_byte(&mut self.i2c, self.address, MPU_CONFIG, 0x03)?;
        // set sample rate
        write_byte(&mut self.i2c, self.address, SMPLRT_DIV, 0x03)?;

        let mut c= read_byte(&mut self.i2c, self.address,  GYRO_CONFIG)?;
        c = c & !0x03; // Clear Fchoice bits [1:0]
        c = c & !0x18; // Clear GFS bits [4:3]
        c = c | 3 << 3; // Set 2000dps full scale range for the gyro (11 on 4:3)
        write_byte(&mut self.i2c, self.address,  GYRO_CONFIG,c)?;

        write_byte(&mut self.i2c, self.address, MPU_CONFIG,  0x03)?;

        write_byte(&mut self.i2c, self.address,  INT_PIN_CFG,0x22)?;
        write_byte(&mut self.i2c, self.address, INT_ENABLE,0x01)?;

        delay_ms(100);
        return Ok(());
    }

    pub fn update(&mut self) -> Result<MpuData, Error> {
        let data_available = read_byte(&mut self.i2c, self.address, INT_STATUS)? & 0x01 > 0;
        if !data_available {
            return Err(Error::NoData);
        }

        let mut imu_count: [i16; 7] = [0; 7];
        let mut raw_data: [u8; 14] = [0; 14]; 

        read_bytes(&mut self.i2c, self.address, ACCEL_XOUT_H, &mut raw_data)?;

        imu_count[0] = ((raw_data[0] as i16) << 8) | (raw_data[1] as i16);
        imu_count[1] = ((raw_data[2] as i16) << 8) | (raw_data[3] as i16);
        imu_count[2] = ((raw_data[4] as i16) << 8) | (raw_data[5] as i16);
        imu_count[3] = ((raw_data[6] as i16) << 8) | (raw_data[7] as i16);
        imu_count[4] = ((raw_data[8] as i16) << 8) | (raw_data[9] as i16);
        imu_count[5] = ((raw_data[10] as i16) << 8) | (raw_data[11] as i16);
        imu_count[6] = ((raw_data[12] as i16) << 8) | (raw_data[13] as i16);

        let ax = (imu_count[0] as f32) * A_RES - self.calibration.accel_bias[0];
        let ay = (imu_count[1] as f32) * A_RES - self.calibration.accel_bias[1];
        let az = (imu_count[2] as f32) * A_RES - self.calibration.accel_bias[2];

        let temp = ((imu_count[3] as f32) / 340.) + 36.53;
        
        let gx = (imu_count[4] as f32) * G_RES - self.calibration.gyro_bias[0];
        let gy = (imu_count[5] as f32) * G_RES - self.calibration.gyro_bias[1];
        let gz = (imu_count[6] as f32) * G_RES - self.calibration.gyro_bias[2];

        return Ok(MpuData {
            accel_x: ax,
            accel_y: ay,
            accel_z: az,
            gyro_x: gx,
            gyro_y: gy,
            gyro_z: gz,
            temp,
        })
    }
}

fn read_byte(i2c: &mut I2c, address: u8, register: u8) -> Result<u8, Error> {
    let mut buf = [0];
    i2c.write_read(address, &[register], &mut buf)?;
    return Ok(buf[0]);
}

fn write_byte(i2c: &mut I2c, address: u8, register: u8, data: u8) -> Result<(), Error> {
    i2c.write(address,&[register, data])?;
    return Ok(())
}

fn read_bytes(i2c: &mut I2c, address: u8, register: u8, data: &mut [u8]) -> Result<(), Error> {
    i2c.write_read(address, &[register], data)?;
    return Ok(())
}
