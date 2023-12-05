import cv2
from cv2 import aruco
import time

cap = cv2.VideoCapture(0)

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

last_print_time = time.time() - 3  # Az utolsó kiírás óta eltelt idő inicializálása

m = -0.00027839979100551
b = -0.32304623355505202

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        gray, aruco_dict, parameters=parameters
    )
    frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow("ArUco Detection", frame_markers)

    current_time = time.time()

    if (
        ids is not None and current_time - last_print_time >= 3
    ):  # Csak 3 másodpercenként
        for i in range(len(ids)):
            marker_id = ids[i][0]
            marker_x = corners[i][0][:, 0].mean()  # A sarkok x koordinátáinak átlaga
            marker_y = corners[i][0][:, 1].mean()  # A sarkok y koordinátáinak átlaga

            print(f"Marker {marker_id}: (x, y) = ({marker_y}, {marker_x})")

            xPosition = marker_y * m + b
            print(f"X Position: {xPosition:.17f}")

        last_print_time = current_time

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
