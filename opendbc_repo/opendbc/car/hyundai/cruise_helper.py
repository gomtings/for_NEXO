from common.numpy_fast import clip, interp
from cereal import car
from common.realtime import DT_CTRL
from common.conversions import Conversions as CV
from opendbc.car.hyundai.values import Buttons
from common.params import Params
from opendbc.car.hyundai.values import CAR
from opendbc.car.isotp_parallel_query import IsoTpParallelQuery
from opendbc.car.hyundai.values import HyundaiFlags
# ajouatom
def enable_radar_tracks(CP, logcan, sendcan):
  print("################ Try To Enable Radar Tracks ####################")
  sccBus = 2 if CP.flags & HyundaiFlags.CAMERA_SCC.value else 0
  rdr_fw = None
  rdr_fw_address = 0x7d0 #
  try:
    try:
      query = IsoTpParallelQuery(sendcan, logcan, sccBus, [rdr_fw_address], [b'\x10\x07'], [b'\x50\x07'], debug=True)
      for addr, dat in query.get_data(0.1).items(): # pylint: disable=unused-variable
        print("ecu write data by id ...")
        new_config = b"\x00\x00\x00\x01\x00\x01"
        #new_config = b"\x00\x00\x00\x00\x00\x01"
        dataId = b'\x01\x42'
        WRITE_DAT_REQUEST = b'\x2e'
        WRITE_DAT_RESPONSE = b'\x68'
        query = IsoTpParallelQuery(sendcan, logcan, sccBus, [rdr_fw_address], [WRITE_DAT_REQUEST+dataId+new_config], [WRITE_DAT_RESPONSE], debug=True)
        result = query.get_data(0)
        print("result=", result)
        break
    except Exception as e:
      print(f"Failed : {e}") 
  except Exception as e:
    print("##############  Failed to enable tracks" + str(e))
  print("################ END Try to enable radar tracks")