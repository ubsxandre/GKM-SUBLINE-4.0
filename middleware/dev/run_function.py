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

  # Nonaktifkan sementara mesin saat membaca data
  conn.disable_device()

  print("Mengambil data attendance...")

  attendance = conn.get_attendance()

  print(f"Jumlah data attendance: {len(attendance)}")

  print("\n=== DATA ATTENDANCE ===")

  for row in attendance:
    print(row)

finally:
  if conn:
    try:
      conn.enable_device()
    except:
      pass

    conn.disconnect()
    print("\nKoneksi ditutup.")