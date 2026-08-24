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
  print(f"Menghubungkan ke {IP_MESIN}:{PORT}...")

  conn = zk.connect()

  print("BERHASIL TERHUBUNG!")

  print("Device Name :", conn.get_device_name())
  print("Serial      :", conn.get_serialnumber())
  print("Firmware    :", conn.get_firmware_version())

except Exception as e:
  print("GAGAL TERHUBUNG")
  print("Error:", type(e).__name__, e)

finally:
  if conn:
    conn.disconnect()
    print("Koneksi ditutup.")