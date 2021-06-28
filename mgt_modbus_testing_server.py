from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform
import socket
import helpers.unit_conversions as unit_con
from helpers.modbus_register_pointers import coil_to_command_lookup, command_to_coil_lookup, command_to_register_lookup, command_to_type_lookup, modbus_type_sizes
import datetime

class dummy_device:
   def __init__(self, device_id):
      # self.host = f"192.168.1.{150+device_id}"
      self.host = "127.0.0.1"
      print(self.host)
      self.port = 502
      self.server = ModbusServer(host=self.host, port=self.port, no_block=True)
      print("Starting server on {}:{}".format(self.host, self.port))
      self.server.start()
      print("Server is online!")

   def write_words(self, command_str, words):
      DataBank.set_words(command_to_register_lookup[command_str], words)
      DataBank.set_bits(command_to_coil_lookup[command_str], [True])

   def send_timeseries(self):
      timeseries = {
         "status": "IDLE",
         "temperature": 24.5123,
         "sesd_voltage": 7.2321,
      }
      words = unit_con.string_to_bytes(timeseries["status"]) + [0 for _ in range(modbus_type_sizes["str"]-len(timeseries["status"]))]
      words += unit_con.pack_bytes_to_register(unit_con.double_to_bytes(timeseries["temperature"]))
      words += unit_con.pack_bytes_to_register(unit_con.double_to_bytes(timeseries["sesd_voltage"]))
      self.write_words("timeseries", words)

   def send_eis_settings(self):
      freq_count = 10
      eis_settings = {
         "freq_count": freq_count, 
         "freq_list": [1000*x for x in range(freq_count)],
         "start_freq": 1000,
         "end_freq": 0,
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
      words += unit_con.pack_bytes_to_register(unit_con.uint32_to_bytes(eis_settings["start_freq"]))
      words += unit_con.pack_bytes_to_register(unit_con.uint32_to_bytes(eis_settings["end_freq"]))
      words += unit_con.pack_bytes_to_register(unit_con.uint32_to_bytes(eis_settings["ptsperdec"]))
      words += unit_con.pack_bytes_to_register(unit_con.uint32_to_bytes(eis_settings["ocv_ms"]))
      words += unit_con.pack_bytes_to_register(unit_con.uint32_to_bytes(eis_settings["sample_ms"]))
      words += unit_con.uint8_to_bytes(eis_settings["periods"])
      words += unit_con.string_to_bytes(eis_settings["bid"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_settings["bid"]))]
      self.write_words("eis_settings", words)
      
   def send_eis_done(self):
      eis_done_info = {
         "temperature": 24.2141,
         "date": datetime.datetime.now().strftime("%m/%d/%Y"),
         "time": datetime.datetime.now().strftime("%H:%M"),
         "voltage": 12.12341,
         "operator": "Testing ReJouligan",
         "project": "Test EIS",
         "bid": "152234-F-R-23-CELL-2",
      }    
      words = unit_con.pack_bytes_to_register(unit_con.double_to_bytes(eis_done_info["temperature"]))
      words += unit_con.string_to_bytes(eis_done_info["date"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["date"]))]
      words += unit_con.string_to_bytes(eis_done_info["time"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["time"]))]
      words += unit_con.pack_bytes_to_register(unit_con.double_to_bytes(eis_done_info["voltage"]))
      words += unit_con.string_to_bytes(eis_done_info["operator"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["operator"]))]
      words += unit_con.string_to_bytes(eis_done_info["project"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["project"]))]
      words += unit_con.string_to_bytes(eis_done_info["bid"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["bid"]))]
      self.write_words("eis_done", words)

   def send_file_logging_settings(self):
      eis_done_info = {
         "eis_filename": "eis_file.rjeis",
         "eis_title": "test EIS title",
         "eis_tag": "EIS Tag",
         "eis_notes": "hi there this is russell\nthe is another line",
         "operator": "Testing ReJouligan",
         "project": "Test EIS",
      }    
      words = unit_con.string_to_bytes(eis_done_info["eis_filename"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["eis_filename"]))]
      words += unit_con.string_to_bytes(eis_done_info["eis_title"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["eis_title"]))]
      words += unit_con.string_to_bytes(eis_done_info["eis_tag"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["eis_tag"]))]
      words += unit_con.string_to_bytes(eis_done_info["eis_notes"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["eis_notes"]))]
      words += unit_con.string_to_bytes(eis_done_info["operator"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["operator"]))]
      words += unit_con.string_to_bytes(eis_done_info["project"]) + [0 for _ in range(modbus_type_sizes["str"]-len(eis_done_info["project"]))]
      self.write_words("file_logging_settings", words)

   def run(self):
      try:
         while True:
            _ = input()
            print("Sending Timeseries...")
            self.send_timeseries()
            sleep(3)
            print("Sending EIS Settings...")
            self.send_eis_settings()
            sleep(3)
            print("Sending EIS Done...")
            self.send_eis_done()
            sleep(3)
            # print("Sending EIS Done...")
            # self.send_eis_done()
            # sleep(3)
            print("Sending File Logging Settings...")
            self.send_file_logging_settings()
            print("COMPLETE")

            
      except KeyboardInterrupt:
         print("Shutdown Server...")
         self.server.stop()
         print("Server is offline.")


dummy_pi = dummy_device(15)
dummy_pi.run()

