from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform

host = '192.168.0.159'
port = 12345
server = ModbusServer(host, port, no_block=True)

try:
   print("Starting server...")
   server.start()
   print("Server is online!")
   state = [0]
   while True:
      DataBank.set_words(0, [int(uniform(0, 100))])
      if state != DataBank.get_words(1):
         state = DataBank.get_words(1)
         print("Value of register 1 has changed to {}".format(state))
         sleep(0.5)
except KeyboardInterrupt:
   print("Shutdown Server...")
   server.stop()
   print("Server is offline.")