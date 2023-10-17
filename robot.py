import rtde_control
import rtde_receive
import rtde_io
import time
import subprocess
import math

pi = math.pi

host = "192.168.98.6"
port = 30004

# control
rtde_c = rtde_control.RTDEControlInterface(host)
# getPosition
rtde_r = rtde_receive.RTDEReceiveInterface(host)
# gripper
rtde_io = rtde_io.RTDEIOInterface(host)

if __name__ == "__main__":
    # p[1] += 0.01         #x tengely fix (előre, hátra)
    # p[2] -= 0.01         #y tengely fix (fel, le)
    # p[3] -= 0.1
    # p[4] += 0.1
    # p[5] += 0.1
    # p[6] += 0.1

    velocity = 0.1
    acceleration = 0.1

    # TARGET = [Base, Shoulder, Elbow, Wrist1, Wrist2, Wrist3]

    home_position = [0, -pi / 2, 0, -pi / 2, 0, 0]
    rtde_c.moveJ(home_position, velocity, acceleration)

    # target1 = [0, -pi / 3, 0, -pi / 2, 0, 0]
    # rtde_c.moveJ(target1, velocity, acceleration)

    # target2 = [0, -pi / 3, pi / 3, -pi / 2, 0, 0]
    # rtde_c.moveJ(target2, velocity, acceleration)

    # target3 = [0, -pi / 3, pi / 3, -pi / 2, -pi / 2, 0]
    # rtde_c.moveJ(target3, velocity, acceleration)

    # target4 = [0, -pi / 3, pi / 3, -pi / 2, -pi / 2, pi]
    # target4 = [0, -pi / 3, pi / 3, -pi / 2, -pi / 2, 3.99455]
    # rtde_c.moveJ(target4, velocity, acceleration)

    p = rtde_r.getActualTCPPose()
    print(f"pose {p}")
    target5 = p
    # target5[0] -= 0.01  # x koordináta
    target5[0] = -0.44756054008226637
    # target5[1] -= 0.01  # y koordináta
    target5[2] -= 0.1  # z koordináta
    # rtde_c.moveL(target5, velocity, acceleration)

    # target1 = [-0.015, -0.935, 0.85, -1.5, 4.75, 1.6]
    # target3 = [3, -0.935, 1.2, -1.85, 4.75, 1.6]

    # rtde_io.setStandardDigitalOut(0, False)

    # rtde_c.moveJ(target1, velocity, acceleration)

    # subprocess.call(["python", "fp_elinditas.py"])

    # p = rtde_r.getActualTCPPose()
    ##print(f"pose {p}")
    # target2 = p
    # target2[2] -= 0.1

    # rtde_c.moveL(target2, velocity, acceleration)

    # rtde_io.setStandardDigitalOut(0, True)

    # rtde_c.moveJ(target1, velocity, acceleration)
    # rtde_c.moveJ(target3, velocity, acceleration)

    # p = rtde_r.getActualTCPPose()
    ##print(f"pose {p}")
    # target4 = p
    # target4[2] -= 0.06

    # rtde_c.moveL(target4, velocity, acceleration)
    # rtde_io.setStandardDigitalOut(0, False)

    rtde_c.stopScript()
