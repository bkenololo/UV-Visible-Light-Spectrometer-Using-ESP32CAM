import cv2 
import numpy as np
import matplotlib.pyplot as plt
import urllib.request

def ambil_gambar_esp32(ip_address="172.20.10.6"):
    """Mengambil 1 gambar snapshot dari ESP32-CAM dan mengembalikannya sebagai array."""
    try:
        url = f"http://{ip_address}/capture"
        print(f"Mengambil gambar dari {url} ...")
        resp = urllib.request.urlopen(url)
        image_data = resp.read()
        img_array = np.asarray(bytearray(image_data), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print("Gagal mengambil gambar:", e)
        return None

def main():
    ip_esp32 = "172.20.10.6"  # Ganti sesuai IP ESP32-CAM kamu
    frame = ambil_gambar_esp32(ip_esp32)

    if frame is None:
        print("Gagal mendapatkan gambar dari ESP32-CAM.")
        return

    roi_selected = False
    r = None

    while True:
        temp_frame = frame.copy()
        k = cv2.waitKey(1)

        if k & 0xFF == ord('r'):
            r = cv2.selectROI("Pilih ROI", temp_frame)
            roi_selected = True

        elif k & 0xFF == ord('s') and roi_selected:
            cropped = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

            # Rotate counter-clockwise 90 derajat biar spektrum horizontal
            cropped = cv2.rotate(cropped, cv2.ROTATE_90_COUNTERCLOCKWISE)
            shape = cropped.shape

            r_dist, g_dist, b_dist, i_dist = [], [], [], []

            num_cols = shape[1]
            wavelengths = np.linspace(400, 700, num_cols)  # 400-700nm mapping

            for i in range(num_cols):
                r_val = np.mean(cropped[:, i, 2])  # Red
                g_val = np.mean(cropped[:, i, 1])  # Green
                b_val = np.mean(cropped[:, i, 0])  # Blue
                i_val = (r_val + g_val + b_val) / 3

                r_dist.append(r_val)
                g_dist.append(g_val)
                b_dist.append(b_val)
                i_dist.append(i_val)

            # Tampilkan hasil dalam 1 window
            fig, axs = plt.subplots(2, 1, figsize=(10, 6))
            axs[0].imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
            axs[0].axis('off')
            axs[0].set_title("Gambar Spektrum (Rotated)")

            axs[1].plot(wavelengths, r_dist, 'r', label='Red')
            axs[1].plot(wavelengths, g_dist, 'g', label='Green')
            axs[1].plot(wavelengths, b_dist, 'b', label='Blue')
            axs[1].plot(wavelengths, i_dist, 'k', label='Intensity')
            axs[1].set_xlabel("Wavelength (nm)")
            axs[1].set_ylabel("Intensity")
            axs[1].set_title("Spectral Distribution")
            axs[1].legend(loc="upper right")
            axs[1].grid(True)

            plt.tight_layout()
            plt.show()

        elif k & 0xFF == ord('q'):
            break

        if roi_selected:
            cropped = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            cv2.imshow('ROI', cropped)
        else:
            cv2.imshow('Foto dari ESP32-CAM', frame)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()