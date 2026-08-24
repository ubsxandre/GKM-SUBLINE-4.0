from zk import ZK
from datetime import datetime
import pandas as pd

IP_MESIN = "192.168.43.201"
PORT = 4370

zk = ZK(
  IP_MESIN,
  port=PORT,
  timeout=10,
  password=0,
  force_udp=False,
  ommit_ping=False
)

conn = None

try:
  conn = zk.connect()
  print("Berhasil terhubung")

  conn.disable_device()

  attendance = conn.get_attendance()

  data = []

  for row in attendance:
      data.append({
          "user_id": row.user_id,
          "timestamp": row.timestamp,
          "status": row.status,
          "punch": row.punch
      })

  df = pd.DataFrame(data)

  print(df)

finally:
  if conn:
    conn.enable_device()
    conn.disconnect()