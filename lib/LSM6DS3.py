import math

import Adafruit_GPIO.I2C as I2C

from .LSM6DS3_CONST import *

address = 0x6b


class LSM6DS3:
    i2c = None
    tempvar = 0

    def __init__(self, address=0x6b, debug=0, pause=0.8):
        self.i2c = I2C.get_i2c_device(address)
        self.address = address

        self.setupAccl()
        self.setupGyro()

        # setup gyro

        self.accel_center_x = self.i2c.readS16(LSM6DS3_XG_OUT_X_L_XL)
        self.accel_center_y = self.i2c.readS16(LSM6DS3_XG_OUT_Y_L_XL)
        self.accel_center_z = self.i2c.readS16(LSM6DS3_XG_OUT_Z_L_XL)

    def setupAccl(self):
        dataToWrite = 0  # Start Fresh!
        dataToWrite |= 0x03  # set at 50hz, bandwidth
        dataToWrite |= 0x00  # 2g accel range
        dataToWrite |= 0x10  # 13hz ODR
        self.i2c.write8(0X10, dataToWrite)  # writeRegister(LSM6DS3_ACC_GYRO_CTRL2_G, dataToWrite)

    def setupGyro(self):
        # Gyro setup

        gy_odr = '13HZ'
        gy_full_scale_dps = '2000'

        tmp = self.i2c.readU8(LSM6DS3_XG_CTRL2_G)
        tmp &= ~LSM6DS3_G_ODR['MASK']
        tmp |= LSM6DS3_G_ODR[gy_odr]
        tmp &= ~LSM6DS3_G_FS['MASK']
        tmp |= LSM6DS3_G_FS[gy_full_scale_dps]
        self.i2c.write8(LSM6DS3_XG_CTRL2_G, tmp)

        # Axis selection
        gy_axis_en = 'XYZ'

        tmp = self.i2c.readU8(LSM6DS3_XG_CTRL10_C)
        tmp &= ~LSM6DS3_G_AXIS_EN['MASK']
        tmp |= LSM6DS3_G_AXIS_EN['X'] if 'X' in gy_axis_en else 0
        tmp |= LSM6DS3_G_AXIS_EN['Y'] if 'Y' in gy_axis_en else 0
        tmp |= LSM6DS3_G_AXIS_EN['Z'] if 'Z' in gy_axis_en else 0
        self.i2c.write8(LSM6DS3_XG_CTRL10_C, tmp)

    def readRawAccelX(self):
        output = self.i2c.readS16(LSM6DS3_XG_OUT_X_L_XL)
        return output

    def readRawAccelY(self):
        output = self.i2c.readS16(LSM6DS3_XG_OUT_Y_L_XL)
        return output

    def readRawAccelZ(self):
        output = self.i2c.readS16(LSM6DS3_XG_OUT_Z_L_XL)
        return output

    def calcAnglesXY(self):
        # Using x y and z from accelerometer, calculate x and y angles
        x_val = 0
        y_val = 0
        z_val = 0
        result = 0

        x2 = 0
        y2 = 0
        z2 = 0
        x_val = self.readRawAccelX() - self.accel_center_x
        y_val = self.readRawAccelY() - self.accel_center_y
        z_val = self.readRawAccelZ() - self.accel_center_z

        x2 = x_val * x_val
        y2 = y_val * y_val
        z2 = z_val * z_val

        result = math.sqrt(y2 + z2)
        if (result != 0):
            result = x_val / result
        accel_angle_x = math.atan(result)
        return accel_angle_x

    def readRawGyroX(self):
        output = self.i2c.readS16(0X22)
        return output

    def readRawGyroY(self):
        output = self.i2c.readS16(0X22)
        return output

    def readRawGyroZ(self):
        output = self.i2c.readS16(0X26)
        return output

    def readFloatGyroX(self):
        output = self.calcGyro(self.readRawGyroX())
        return output

    def calcGyroXAngle(self):
        temp = 0
        temp += self.readFloatGyroX()
        if (temp > 3 or temp < 0):
            self.tempvar += temp
        return self.tempvar

    def calcGyro(self, rawInput):
        gyroRangeDivisor = 245 / 125  # 500 is the gyro range (DPS)
        output = rawInput * 4.375 * (gyroRangeDivisor) / 1000
        return output
