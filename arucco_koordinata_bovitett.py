import cv2
from cv2 import aruco
import time
import math

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

    current_time = time.time()  # Inicializáld a current_time változót

    if ids is not None and current_time - last_print_time >= 3:
        for i in range(len(ids)):
            marker_id = ids[i][0]
            marker_x = corners[i][0][:, 0].mean()
            marker_y = corners[i][0][:, 1].mean()

            print(f"Marker {marker_id}: (x, y) = ({marker_x}, {marker_y})")

            xPosition = marker_x * m + b
            print(f"X Position: {xPosition:.17f}")

            # Kiírja a marker 4 sarkának koordinátáit
            print(f"Marker {marker_id} sarkai:")
            for corner in corners[i][0]:
                x, y = corner
                print(f"    (x, y) = ({x}, {y})")

            # Elforgatottság
            tl_x, tl_y = corners[i][0][0]
            tr_x, tr_y = corners[i][0][1]

            angle = math.degrees(math.atan2(tr_y - tl_y, tr_x - tl_x))
            radians = (angle) * (math.pi / 180)
            radians += math.pi
            print(f"{radians } radián")

        last_print_time = current_time

    cv2.imshow("ArUco Detection", frame_markers)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
