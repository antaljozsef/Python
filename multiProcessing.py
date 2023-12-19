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


# ---------- FÜGVÉNYEK


# Motorvezérlő
def control_motor():
    def ticcmd(*args):
        return subprocess.check_output(["ticcmd"] + list(args))

    try:
        # A motor elíndítása
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


# ArUco Kamera
def detect_and_display_aruco(cameraEvent, arucco_target_event, queue):
    # Kamera inicializálása
    cap = cv2.VideoCapture(0)

    # Kamera inicializáció ellenőrzése
    if not cap.isOpened():
        print("Kamera hiba")
        return

    # Várakoztatjuk a Kamera process-t
    cameraEvent.wait()

    # ArUco szótár létrehozása
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

    # Egyenes egyenletéhez tartozó értékek
    m = -0.0002382995890505  # Meredekség
    b = -0.3083860187200043

    while cameraEvent.is_set():
        # Kamera képének beolvasása
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # ArUco marker detektálása
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, aruco_dict, parameters=parameters
        )
        frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)

        if ids is not None:
            for i in range(len(ids)):
                # Marker azonosító és középpont koordináták kiszámítása
                marker_id = ids[i][0]
                marker_x = corners[i][0][:, 0].mean()
                marker_y = corners[i][0][:, 1].mean()

                # Kiírás a konzolra
                print(f"Marker {marker_id}: (x, y) = ({marker_y}, {marker_x})")

                # X koordináta számolása az egyenes egyenlete alapján
                xPosition = marker_y * m + b

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

                # Az utolsó csuklohoz, hogy ne forduljon sokszor körbe
                if 0 < radian < 1:
                    radian = math.pi / 2 + radian

                if -2 < radian < 0:
                    radian = math.pi + radian

                if radian > 1:
                    radian = math.pi / 2 + radian

                if radian < -2:
                    radian = 2 * math.pi + radian

                # X koordináta, és szög átadása
                queue.put(np.array([xPosition, radian]))

                # Robotkar process elindítása
                arucco_target_event.set()

                # Kamera process leállítása
                cameraEvent.clear()

        # Kép megjelenítése
        cv2.imshow("ArUco Detection", frame_markers)

        # Kilépési feltétel (q gomb megnyomása)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Kamera leállítása és ablakok bezárása
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

        velocity = 3
        acceleration = 3

        home_position = [0, -pi / 2, 0, -pi / 2, 0, 0]
        # rtde_c.moveJ(home_position, velocity, acceleration)

        waiting_position = [0, -pi / 2, pi / 2, -pi / 2, -pi / 2, pi]
        rtde_c.moveJ(waiting_position, velocity, acceleration)

        # Gripper kinyitása
        rtde_ioo.setStandardDigitalOut(0, False)

        # Kamera process elindítása
        cameraEvent.set()

        p = rtde_r.getActualTCPPose()
        x_axis_displacement = p

        if queue.empty():
            arucco_target_event.wait()

        item = queue.get()

        # start_time = time.time() -- robotkar mozgási idejének leméréséhez kellet

        x_axis_displacement[0] = item[0]
        rtde_c.moveL(x_axis_displacement, velocity, acceleration)

        p = rtde_r.getActualQ()
        final_joint_rotation = p

        final_joint_rotation[5] = item[1]
        rtde_c.moveJ(final_joint_rotation, velocity, acceleration)

        # A darab fölé mozgatás
        pz = rtde_r.getActualTCPPose()
        z_axis_displacement = pz
        z_axis_displacement[2] -= 0.11  # z koordináta
        rtde_c.moveL(z_axis_displacement, velocity, acceleration)

        # current_time = time.time() -- robotkar mozgási idejének leméréséhez kellet
        # elapsed_time = current_time - start_time
        # print(f"Robotkar mozgasi ideje: {elapsed_time}")

        # 1.8 másodpercet kell várjon a robot, amig a darab odaér a gripperhez
        time.sleep(1.8)

        # Darab megfogása
        p = rtde_r.getActualTCPPose()
        gripping_item_position = p
        gripping_item_position[2] -= 0.02  # z koordináta
        rtde_c.moveL(gripping_item_position, velocity, acceleration)

        # Gripper becsukása
        rtde_ioo.setStandardDigitalOut(0, True)

        # Darab felemelése
        rtde_c.moveL(x_axis_displacement, velocity, acceleration)

        # rtde_c.stopScript()

    except Exception as e:
        print("Robotkar hiba")
        print(e)


if __name__ == "__main__":
    # Események
    cameraEvent = multiprocessing.Event()
    arucco_target_event = multiprocessing.Event()

    # Queue Létrehozása
    queue = multiprocessing.Queue()

    # Létrehozunk 3 folyamatot
    FutoszalagProcess = multiprocessing.Process(target=control_motor)

    KameraProcess = multiprocessing.Process(
        target=detect_and_display_aruco,
        args=(
            cameraEvent,
            arucco_target_event,
            queue,
        ),
    )
    RobotProcess = multiprocessing.Process(
        target=move_robot_arm,
        args=(
            cameraEvent,
            arucco_target_event,
            queue,
        ),
    )

    # Párhuzamos folyamatok indítása
    FutoszalagProcess.start()
    KameraProcess.start()
    RobotProcess.start()

    # Párhuzamos folyamatok befejezése
    FutoszalagProcess.join()
    KameraProcess.join()
    RobotProcess.join()

    print("Fő folyamat befejezve")
