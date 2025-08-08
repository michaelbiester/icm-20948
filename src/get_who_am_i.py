# get_who_am_i.py

from smbus2 import SMBus

ic2bus = SMBus(1)

I2C_ADDR = 0x69
WHO_AM_I = 0x00
BANK_SEL = 0x7f

bank = 0
ic2bus.write_byte_data(I2C_ADDR, BANK_SEL, bank)
chip_id = ic2bus.read_byte_data(I2C_ADDR, WHO_AM_I)
print(f"who_am_i: {hex(chip_id)}")

