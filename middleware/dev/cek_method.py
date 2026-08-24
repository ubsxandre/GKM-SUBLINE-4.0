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
  conn = zk.connect()
  print("Berhasil terhubung")
  conn.disable_device()
  attendance = conn.get_attendance()

  # print("=== METHOD CONNECTION ===")
  # for name in dir(conn):
  #   if not name.startswith("_"):
  #     print(name)

  # for name in dir(conn):
  #   if "short" in name.lower() or "work" in name.lower():
  #       print(name)

  # print("=== WORK CODE ===")
  # for name in dir(conn):
  #   if "work" in name.lower():
  #       print(name)

  # print("=== Get Attendance ===")
  # attendance = conn.get_attendance()
  # for row in attendance[-10:]:
  #   print("=" * 60)
  #   print("OBJECT :", row)
  #   print("VARS   :", vars(row))
  #   print("=" * 60)

  # print("=== Get Platform ===")
  # print("Platform :", conn.get_platform())
  # print("Firmware :", conn.get_firmware_version())
  # print("Device   :", conn.get_device_name())

  for row in attendance[-10:]:
    print(vars(row))
finally:
  if conn:
    conn.disconnect()