from pyModbusTCP.client import ModbusClient
from time import sleep

# Modbus Function Codes
# 1 - Read Coil Status
# 2 - Read Input Status
# 3 - Read Holding Registers
# 4 - Read Input Resgiters
# 5 - Write Single Coil Status
# 6 - Write Single Register
# 15 - Multiple Coil Write
# 16 - Multiple Register Write

# Modbus Register Map Sets
# 00001-09999 - Coils               (read/write)      (1-bit)
# 10001-19999 - Discrete Inputs     (read only)       (1-bit)
# 30001-39999 - Input Registers     (read only)       (16-bit)
# 40001-49999 - Holding Registers   (read/write)      (16-bit)


client = ModbusClient(host='192.168.0.159', port=12345)
client.open()
for i in range(5):
   sleep(1)
   print("Reading Holding Register 0: {}".format(client.read_holding_registers(0)))
   client.write_single_register(1, i)
   print("Reading Holding Register 0: {}".format(client.read_holding_registers(1)))