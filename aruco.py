import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

# ArUco szótár inicializálása
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# Üres ábra inicializálása
fig = plt.figure()

# Rács méretezése
nx = 4
ny = 3

# Rács bejárása és ArUco markerek generálása
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny, nx, i)
    img = aruco.drawMarker(aruco_dict, i, 700)
    plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
    ax.axis("off")

# Markerek mentése PDF formátumban
#plt.savefig("markers.pdf")
#plt.show()

# Kép beolvasása
frame = cv2.imread("aruco_photo.png")

# Kép megjelenítése
plt.figure()
plt.imshow(frame)
plt.show()

# Szürkeárnyalatos konverzió
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Detektálási paraméterek inicializálása
parameters = aruco.DetectorParameters_create()

# ArUco markerek detektálása a képen
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

# Markerek jelölése a képen
frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

# Jelölt markerek megjelenítése
plt.figure()
plt.imshow(frame_markers)

# Azonosítók középpontjainak kirajzolása
for i in range(len(ids)):
    c = corners[i][0]
    plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label="id={0}".format(ids[i]))

# Azonosítók feliratozása
plt.legend()
plt.show()