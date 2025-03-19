import cv2
import numpy as np

# Yüz tespiti için Haar Cascade yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Video kaynağını aç (Dosya veya Kamera)
video_capture =  cv2.VideoCapture(0)  # Eğer webcam kullanacaksan "0" yaz

# Panda yüzü maskesini yükle
panda_mask = cv2.imread("M6L3\pngegg (2).png", cv2.IMREAD_UNCHANGED)  # Saydam PNG olmalı

while True:
    ret, frame = video_capture.read()
    if not ret:
        break  # Video bittiğinde çık

    # Gri tonlamaya çevir ve yüzleri bul
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Panda yüzünü yüz boyutuna göre yeniden boyutlandır
        resized_mask = cv2.resize(panda_mask, (w, h))

        # Alfa kanalı kullanarak panda yüzünü ekle
        for i in range(h):
            for j in range(w):
                if resized_mask[i, j, 3] > 0:  # Alfa kanalı kontrolü (0 ise saydam)
                    frame[y + i, x + j] = resized_mask[i, j][:3]

    # Sonucu göster
    cv2.imshow("Panda Maskeli Video", frame)

    # 'q' tuşuna basılınca çık
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Temizlik
video_capture.release()
cv2.destroyAllWindows()