import multiprocessing
import subprocess
import cv2
from cv2 import aruco
import time
import math
import rtde_control
import rtde_receive
import rtde_io

# ---------- ARUCCO

cap = cv2.VideoCapture(0)

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

last_print_time = time.time() - 3  # Az utolsó kiírás óta eltelt idő inicializálása

m = -0.00027839979100551
b = -0.32304623355505202

# ---------- ROBOT

pi = math.pi

host = "192.168.98.6"
port = 30004

# control
rtde_c = rtde_control.RTDEControlInterface(host)
# getPosition
rtde_r = rtde_receive.RTDEReceiveInterface(host)
# gripper
rtde_io = rtde_io.RTDEIOInterface(host)

# ---------- FÜGVÉNYEK

# Motorvezérlő
def control_motor():
    def ticcmd(*args):
        return subprocess.check_output(["ticcmd"] + list(args)

    # TIC motorvezérlő inicializálása
    ticcmd("--exit-safe-start")

    # Állítsuk be a velocity-t -40000000-re
    ticcmd("--velocity", "-40000000")

    # Kezdő időpont
    start_time = time.time()

    while True:
        # Motor bekapcsolása
        ticcmd("--energize")

        # Idő ellenőrzése
        current_time = time.time()
        elapsed_time = current_time - start_time

        # Ellenőrzés, hogy eltelt-e már 17 másodperc
        if elapsed_time >= 17:
            break

    # Motor kikapcsolása
    ticcmd("--deenergize")

# ArUco
def detect_and_display_aruco():
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters
        )
        frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)

        current_time = time.time()

        if ids is not None and current_time - last_print_time >= 3:
            for i in range(len(ids)):
                marker_id = ids[i][0]
                marker_x = corners[i][0][:, 0].mean()
                marker_y = corners[i][0][:, 1].mean()

                print(f"Marker {marker_id}: (x, y) = ({marker_x}, {marker_y}")

                xPosition = marker_x * m + b
                print(f"X Position: {xPosition:.17f}")

                print(f"Marker {marker_id} sarkai:")
                for corner in corners[i][0]:
                    x, y = corner
                    print(f"    (x, y) = ({x}, {y})")

                tl_x, tl_y = corners[i][0][0]
                tr_x, tr_y = corners[i][0][1]

                angle = math.degrees(math.atan2(tr_y - tl_y, tr_x - tl_x))
                rad = angle * (math.pi / 180)
                rad += math.pi
                print(f"{rad} radián")

            last_print_time = current_time

        cv2.imshow("ArUco Detection", frame_markers)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Függvény egy egyszerű üzenet nyomtatásához
def move_robot_arm():
    
    velocity = 0.1
    acceleration = 0.1

    home_position = [0, -pi / 2, 0, -pi / 2, 0, 0]
    #rtde_c.moveJ(home_position, velocity, acceleration)
    
    # target4 = [0, -pi / 3, pi / 3, -pi / 2, -pi / 2, pi]
    # target4 = [0, -pi / 3, pi / 3, -pi / 2, -pi / 2, 3.99455]
    # rtde_c.moveJ(target4, velocity, acceleration)

    p = rtde_r.getActualTCPPose()
    target5 = p
    target5[0] = xPosition
    target5[1] = rad
    target5[2] -= 0.1
    #rtde_c.moveL(target5, velocity, acceleration)
    
    # rtde_io.setStandardDigitalOut(0, False)
    # rtde_io.setStandardDigitalOut(0, True)

    rtde_c.stopScript()

if __name__ == "__main__":
    # Létrehozunk 3 folyamatot
    process1 = multiprocessing.Process(target=control_motor)
    process2 = multiprocessing.Process(target=detect_and_display_aruco)
    process3 = multiprocessing.Process(target=move_robot_arm, args=(xPosition, rad))

    # Párhuzamos folyamatok indítása
    process1.start()
    process2.start()
    process3.start()

    # Párhuzamos folyamatok befejezése
    process1.join()
    process2.join()
    process3.join()

    print("Fő folyamat befejezve.")
