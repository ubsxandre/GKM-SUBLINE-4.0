from zk import ZK

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

  print("BERHASIL TERHUBUNG\n")

  print("=== METHOD CONNECTION ===")

  for name in dir(conn):
    if not name.startswith("_"):
      print(name)

finally:
  if conn:
    conn.disconnect()