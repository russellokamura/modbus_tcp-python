from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform
import socket
import helpers.unit_conversions as unit_con
from helpers.modbus_register_pointers import coil_to_command_lookup, command_to_coil_lookup, command_to_register_lookup, command_to_type_lookup, modbus_type_sizes


class dummy_device:
   def __init__(self, device_id):
      self.host = f"192.168.1.{150+device_id}"
      self.port = 502
      self.server = ModbusServer(self.host, self.port, no_block=True)
      print("Starting server on {}:{}".format(self.host, self.port))
      self.server.start()
      print("Server is online!")

   def send_timeseries(self):
      timeseries = {
         "status": "IDLE",
         "temperature": 24.5123,
         "sesd_voltage": 7.2321,
      }
      words = unit_con.string_to_bytes(timeseries["status"]) + [0 for _ in range(modbus_type_sizes["str"]-len(timeseries["status"]))]
      words += unit_con.pack_bytes_to_register(unit_con.double_to_bytes(timeseries["temperature"]))
      words += unit_con.pack_bytes_to_register(unit_con.double_to_bytes(timeseries["sesd_voltage"]))
      DataBank.set_words(command_to_register_lookup["timeseries"], words)
      DataBank.set_bits(command_to_coil_lookup["timeseries"], [False])

   def send_eis_settings(self):
      freq_count = 10
      eis_settings = {
         "freq_count": freq_count, 
         "freq_list": [1000*x for x in range(freq_count)],
         "start_freq": 1000.0,
         "end_freq": 0.1,
         "ptsperdec": 10,
         "ocv_ms": 10000,
         "sample_ms": 1000,
         "periods": 10,
         "bid": "154613-F-L-23-CELL-2",
      }
      words = unit_con.pack_bytes_to_register(unit_con.uint32_to_bytes(eis_settings["freq_count"]))
      for i in range(eis_settings["freq_count"]):
         words += unit_con.pack_bytes_to_register(unit_con.uint32_to_bytes(eis_settings["freq_list"][i]))
      words += [0, 0] * (100-eis_settings["freq_count"])
      words += 
      words += unit_con.pack_bytes_to_register(unit_con.double_to_bytes(eis_settings["temperature"]))
      words += unit_con.pack_bytes_to_register(unit_con.double_to_bytes(eis_settings["sesd_voltage"]))

      DataBank.set_words(command_to_register_lookup["eis_settings"], words)
      DataBank.set_bits(command_to_coil_lookup["eis_settings"], [False])

   def run(self):
      try:
         while True:
            if state != DataBank.get_words(1):
               state = DataBank.get_words(1)
               print("Value of register 1 has changed to {}".format(state))
               sleep(0.5)
      except KeyboardInterrupt:
         print("Shutdown Server...")
         self.server.stop()
         print("Server is offline.")


dummy_pi = dummy_device(15)
dummy_pi.run()

