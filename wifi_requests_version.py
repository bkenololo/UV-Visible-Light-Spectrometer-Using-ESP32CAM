import requests
import numpy as np
import cv2

def ambil_gambar(ip_address="192.168.1.44"):
    try:
        print(f"Mengambil gambar dari http://{ip_address}/capture ...")
        response = requests.get(f"http://{ip_address}/capture", timeout=5)
        image_data = response.content

        print(f"Ukuran gambar diterima: {len(image_data)} bytes")

        img_array = np.asarray(bytearray(image_data), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            print("Gagal decode gambar")
        return img
    except Exception as e:
        print("Gagal mengambil gambar:", e)
        return None

img = ambil_gambar()
if img is not None:
    cv2.imshow("ESP32-CAM", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
