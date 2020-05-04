#!/usr/bin/env python3
import traceback

import cereal.messaging as messaging
from panda.python.uds import FUNCTIONAL_ADDRS
from selfdrive.car.isotp_parallel_query import IsoTpParallelQuery
from selfdrive.swaglog import cloudlog
import time

VIN_REQUEST = b'\x09\x02'
VIN_RESPONSE = b'\x49\x02\x01'
VIN_UNKNOWN = "0" * 17

def vin_check_digit_validator(vin):
  if len(vin) <= 8:
    return False

  key = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5,
         "F": 6, "G": 7, "H": 8, "J": 1, "K": 2,
         "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
         "S": 2, "T": 3, "U": 4, "V": 5, "W": 6,
         "X": 7, "Y": 8, "Z": 9, "0": 0, "1": 1,
         "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
         "7": 7, "8": 8, "9": 9}

  weight = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

  check_digit_key = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
                     "6": 6, "7": 7, "8": 8, "9": 9, "X": 10}

  products = 0
  for i, char in enumerate(vin):
    products += key[char] * weight[i]

  if vin[8] not in check_digit_key:
    return False

  if (products % 11 == check_digit_key[vin[8]]):
    return True
  return False

def listen_for_gm_vin(logcan, timeout=1.5):
  # GM is missing the first char from the VIN, look it up from the first two we do have
  # This will probably cause problems with GM cars built in mexico...
  # We might need to update this to have several options and use the check digit to figure out
  # which one is correct
  GM_FIRST_CHAR_LOOKUP = {"GT": "1", "G1": "1" , "G4": "1", "G6": "1", "0L": "W"}

  logcan = messaging.sub_sock('can')
  gm_vin_candidate = "0000000000000000"
  canbus = 1
  part1_id = 0x741
  part1_count = 0
  part2_id = 0x743
  part2_count = 0
  start_time = time.time()
  while True:
    can_recv = messaging.drain_sock(logcan, wait_for_one=True)
    for msgs in can_recv:
      for msg in msgs.can:
        if msg.src == canbus:
          if (msg.address == part1_id):
            gm_vin_candidate = msg.dat.decode("ascii") + gm_vin_candidate[8:]
            part1_count += 1
          if (msg.address == part2_id):
            gm_vin_candidate = gm_vin_candidate[:8] + msg.dat.decode("ascii")
            part2_count += 1

    if time.time() - start_time > timeout:
      break

  gm_vin_candidate = GM_FIRST_CHAR_LOOKUP.get(gm_vin_candidate[:2], "0") + gm_vin_candidate # Region is omitted from GM VIN on CAN Bus
  if vin_check_digit_validator(gm_vin_candidate):
    return gm_vin_candidate
  return VIN_UNKNOWN

def get_vin(logcan, sendcan, bus, timeout=0.1, retry=5, debug=False):
  vin = listen_for_gm_vin(logcan)
  if (vin != VIN_UNKNOWN):
    return 0x741, vin

  for i in range(retry):
    try:
      query = IsoTpParallelQuery(sendcan, logcan, bus, FUNCTIONAL_ADDRS, [VIN_REQUEST], [VIN_RESPONSE], functional_addr=True, debug=debug)
      for addr, vin in query.get_data(timeout).items():
        return addr[0], vin.decode()
      print(f"vin query retry ({i+1}) ...")
    except Exception:
      cloudlog.warning(f"VIN query exception: {traceback.format_exc()}")

  return 0, VIN_UNKNOWN


if __name__ == "__main__":
  import time
  sendcan = messaging.pub_sock('sendcan')
  logcan = messaging.sub_sock('can')
  time.sleep(1)
  addr, vin = get_vin(logcan, sendcan, 1, debug=False)
  print(hex(addr), vin)
