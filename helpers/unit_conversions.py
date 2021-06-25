import struct

def double_to_uint64(dec):
   """Convert a decimal to an unsigned uint64."""
   byte_list = [int(x) for x in struct.pack(">d", dec)]
   last_idx = len(byte_list) - 1
   uint64 = 0
   for i in range(len(byte_list)):
      uint64 += byte_list[last_idx-i] << (8*i)
   return uint64

def uint64_to_double(uint64):
   """Convert a unsigned uint64 to a floating point double decimal value."""
   byte_list = struct.pack(">Q", uint64)
   return struct.unpack(">d", byte_list)[0]

def float_to_uint32(dec):
   """Convert a decimal to an unsigned uint32."""
   byte_list = [int(x) for x in struct.pack(">f", dec)]
   last_idx = len(byte_list) - 1
   uint32 = 0
   for i in range(len(byte_list)):
      uint32 += byte_list[last_idx-i] << (8*i)
   return uint32

def uint32_to_float(uint32):
   """Convert a unsigned uint32 to a floating point single decimal value."""
   byte_list = struct.pack(">L", uint32)
   return struct.unpack(">f", byte_list)[0]

def unsigned_int_to_bytes(num, byte_count, big_endian=True):
   """Convert unsigned integer to list of bytes."""
   byte_list = []
   for i in range(byte_count):
      byte_list.append(num & 0xFF)
      num = num >> 8
   if big_endian:
      return byte_list[::-1]
   else:
      return byte_list

def string_to_bytes(s):
   """Convert a string to list of bytes."""
   return [ord(c) for c in s]

def bytes_to_string(byte_list):
   """
   Convert a list of bytes to a string.
   
   Will ignore values outside of the range (32, 126) 
       which corresponds to characters from`space` to 
       `~` on an ascii table. 
   """
   return "".join([chr(x) for x in byte_list if 32 <= x <=126])

def double_to_bytes(dec):
   """Convert a decimal to a list of 8 bytes (IEEE-754 Double Format)."""
   return unsigned_int_to_bytes(double_to_uint64(dec), 8)

def float_to_bytes(dec):
   """Convert a decimal to a list of 4 bytes (IEEE-754 Single Format)."""
   return unsigned_int_to_bytes(float_to_uint32(dec), 4)

def uint8_to_bytes(num):
   """Convert an integer to a list of 1 byte (char)."""
   return [(num&0xFF)]

def uint16_to_bytes(num):
   """Convert an integer to a list of 2 bytes (short)."""
   return unsigned_int_to_bytes(num, 2)

def uint32_to_bytes(num):
   """Convert an integer to a list of 4 bytes (int)."""
   return unsigned_int_to_bytes(num, 4)

def uint64_to_bytes(num):
   """Convert an integer to a list of 8 bytes (long)."""
   return unsigned_int_to_bytes(num, 8)

def bool_to_bytes(x):
   """Convert a boolean to a list of 1 byte (bool)."""
   return [1] if x else [0]

def char_to_bytes(c):
   """Convert a single character to a list of 1 byte (char)."""
   return [ord(c)]

def concatenate_bytes(byte_list):
   """Return unsigned integer value of bytes"""
   ret_val = 0
   for i in range(len(byte_list)):
      ret_val += byte_list[i] << (8*(len(byte_list)-i-1))
   return ret_val

def bytes_to_double(byte_list):
   """Concatenate and convert a list of bytes to a single double value."""
   assert len(byte_list) == 8, f"Double precision requires 8 bytes. {len(byte_list)} were given."
   return uint64_to_double(concatenate_bytes(byte_list))

def bytes_to_float(byte_list):
   """Concatenate and convert a list of bytes to a single float value."""
   assert len(byte_list) == 4, f"Single precision requires 4 bytes. {len(byte_list)} were given."
   return uint32_to_float(concatenate_bytes(byte_list))

def bytes_to_uint64(byte_list):
   """Concatenate and convert a list of bytes to a single double value."""
   assert len(byte_list) == 8, f"uint64 requires 8 bytes. {len(byte_list)} were given."
   return concatenate_bytes(byte_list)

def bytes_to_uint32(byte_list):
   """Concatenate and convert a list of bytes to a single double value."""
   assert len(byte_list) == 4, f"uint32 requires 4 bytes. {len(byte_list)} were given."
   return concatenate_bytes(byte_list)

def bytes_to_uint16(byte_list):
   """Concatenate and convert a list of bytes to a single double value."""
   assert len(byte_list) == 2, f"uint64 requires 2 bytes. {len(byte_list)} were given."
   return concatenate_bytes(byte_list)

def convert_val_to_bytes(val, byte_count=None):
   """Convert the `val` based on its type.  If it is a float or int, convert based on `byte_count`."""
   if isinstance(val, str):
      return string_to_bytes(val)
   elif isinstance(val, float):
      if byte_count == 8:
         return double_to_bytes(val) 
      elif byte_count == 4:
         return float_to_bytes(val)
      else: 
         raise Exception("Cannot convert float to bytes.")
   elif isinstance(val, int):
      if byte_count == 1:
         return uint8_to_bytes(val)
      elif byte_count == 2:
         return uint16_to_bytes(val) 
      elif byte_count == 4:
         return uint32_to_bytes(val)
      elif byte_count == 8:
         return uint64_to_bytes(val)
      else: 
         raise Exception("Cannot convert int to bytes.")
   else: 
      raise Exception("Unsupported type. Cannot convert to bytes.")

def pack_bytes_to_register(byte_list, bytes_per_register=2):
   """Will package bytes into concatenated list of integers based on number of bytes per register."""
   register_list = []
   assert (len(byte_list) % bytes_per_register) == 0, "Payload is not consistent with expected bytes per register."
   register_index = 1
   current_register = 0
   for byte in byte_list:
      if register_index < bytes_per_register:
         current_register += byte << (8 * (bytes_per_register-register_index))
         register_index += 1
      else:
         current_register += byte
         register_list.append(current_register)
         register_index = 1
         current_register = 0
   return register_list

def unpack_register_to_uint(register_list, bytes_per_register=2):
   """Will concatentate register list to a single unsigned integer."""
   ret_val = 0
   for i in range(len(register_list)):
      ret_val += register_list[i] << (8*bytes_per_register*(len(register_list)-i-1))
   return ret_val