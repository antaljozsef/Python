import multiprocessing
import subprocess
import cv2
from cv2 import aruco
import time
from time import sleep
import math
import rtde_control
import rtde_receive
import rtde_io
import numpy as np
import keyboard


# todo: should move this to config
# todo: X_DEFAULT_POSTION
radian = 0.0
xPosition = 0.0

# todo: should move this to main
queue = multiprocessing.Queue()

# ---------- FÜGVÉNYEK


# Motorvezérlő
def control_motor():
    def ticcmd(*args):
        return subprocess.check_output(["ticcmd"] + list(args))

    try:
        # TIC motorvezérlő inicializálása
        ticcmd("--exit-safe-start")

        # Állítsuk be a velocity-t -40000000-re
        ticcmd("--velocity", "-40000000")

        while True:
            # Motor bekapcsolása
            ticcmd("--energize")

    except subprocess.CalledProcessError as e:
        print("Futoszalag hiba", e)

    # Motor kikapcsolása
    # ticcmd("--deenergize")


# ArUco
def detect_and_display_aruco(cameraEvent, arucco_target_event, queue):
    cap = cv2.VideoCapture(0)

    # Kamera inicializáció ellenőrzése
    if not cap.isOpened():
        print("Kamera hiba")
        return

    cameraEvent.wait()

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    m = 0.0003018053033986
    b = -0.4256262811303743

    while cameraEvent.is_set():
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters
        )
        frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)

        if ids is not None:
            for i in range(len(ids)):
                marker_id = ids[i][0]
                marker_x = corners[i][0][:, 0].mean()
                marker_y = corners[i][0][:, 1].mean()

                print(f"Marker {marker_id}: (x, y) = ({marker_y}, {marker_x})")

                xPosition = marker_y * m + b
                print(f"X Position: {xPosition:.17f}")

                # Kiírja a marker 4 sarkának koordinátáit
                # print(f"Marker {marker_id} sarkai:")
                # for corner in corners[i][0]:
                #     x, y = corner
                #     print(f"    (x, y) = ({x}, {y})")

                # Elforgatottság
                tl_x, tl_y = corners[i][0][0]
                tr_x, tr_y = corners[i][0][1]

                angle = math.degrees(math.atan2(tr_y - tl_y, tr_x - tl_x))
                radian = (angle) * (math.pi / 180)
                # radian += math.pi
                radian = math.fmod(radian, math.pi)
                print(f"{radian} -----radián Arucco1")

                if 0 < radian < 1:
                    radian = math.pi / 2 + radian

                if -2 < radian < -1:
                    radian = math.pi + radian

                if radian > 1:
                    radian = math.pi / 2 + radian

                if radian < -2:
                    radian = 2 * math.pi + radian

                print(f"{radian} -----radián Arucco2")

                # TODO: check data struct from onther codebase: DetectionData
                queue.put(np.array([xPosition, radian]))

                # arucco_target_event.set()
                arucco_target_event.set()

                print("Benne van a queuban")
                # exit()

                # todo: if we need to stop: camere_event.clear()
                cameraEvent.clear()

        cv2.imshow("ArUco Detection", frame_markers)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# Robot
def move_robot_arm(cameraEvent, arucco_target_event, queue):
    try:
        pi = math.pi

        host = "192.168.98.6"
        port = 30004

        # control
        rtde_c = rtde_control.RTDEControlInterface(host)
        # getPosition
        rtde_r = rtde_receive.RTDEReceiveInterface(host)
        # gripper
        rtde_ioo = rtde_io.RTDEIOInterface(host)

        velocity = 0.1
        acceleration = 0.1

        # rtde_ioo.setStandardDigitalOut(0, False)

        home_position = [0, -pi / 2, 0, -pi / 2, 0, 0]
        # rtde_c.moveJ(home_position, velocity, acceleration)

        # waypoints['HomePosition'] = ..
        target4 = [0, -pi / 2, pi / 2, -pi / 2, -pi / 2, pi]
        # target4 = [0, -pi / 3, pi / 3, -pi / 2, -pi / 2, radian]
        rtde_c.moveJ(target4, velocity, acceleration)

        cameraEvent.set()

        # p = rtde_r.getActualTCPPose()

        px = rtde_r.getActualTCPPose()
        target6 = px

        # arucco_target_event.wait()
        # todo: check if queue is empty ==> wait for queue to have at least one item

        if queue.empty():
            arucco_target_event.wait()

        item = queue.get()
        # item = queue.value
        # cameraEvent.clear()

        print(f"x poyicio: {item[0]}")
        print(f"radian: {item[1]}")

        target6[0] = item[0] - 0.015
        rtde_c.moveL(target6, velocity, acceleration)

        p = rtde_r.getActualQ()
        target5 = p

        target5[5] = item[1]
        rtde_c.moveJ(target5, velocity, acceleration)

        pz = rtde_r.getActualTCPPose()
        target7 = pz

        target7[2] -= 0.13  # z koordináta
        rtde_c.moveL(target7, velocity, acceleration)

        test = rtde_r.getActualTCPPose()
        print(f"Vegpont X pozicio teszt: {test[0]}")

        rtde_ioo.setStandardDigitalOut(0, True)

        rtde_c.moveJ(target4, velocity, acceleration)

        # rtde_io.setStandardDigitalOut(0, False)
        # rtde_io.setStandardDigitalOut(0, True)

        # rtde_c.stopScript()

        print("Robotkar program vége")

    except Exception as e:
        print("Robotkar hiba")
        print(e)


if __name__ == "__main__":
    # Események
    cameraEvent = multiprocessing.Event()
    arucco_target_event = multiprocessing.Event()

    # Létrehozunk 3 folyamatot
    # todo: read from config file
    # if [config.get('USE_CONVEYOR']:
    # process1 = multiprocessing.Process(target=control_motor)

    # todo: Processzek elnevezese
    process2 = multiprocessing.Process(
        target=detect_and_display_aruco,
        args=(
            cameraEvent,
            arucco_target_event,
            queue,
        ),
    )
    process3 = multiprocessing.Process(
        target=move_robot_arm,
        args=(
            cameraEvent,
            arucco_target_event,
            queue,
        ),
    )

    # Párhuzamos folyamatok indítása
    # process1.start()
    process2.start()
    process3.start()

    # Párhuzamos folyamatok befejezése
    process2.join()
    # cameraEvent.clear()

    process3.join()

    print("Fő folyamat befejezve")
