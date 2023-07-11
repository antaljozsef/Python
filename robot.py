import rtde_control
import rtde_receive
import rtde_io
import time
import subprocess

host = "192.168.98.6"
port = 30004

# control
rtde_c = rtde_control.RTDEControlInterface(host)
# getPosition
rtde_r = rtde_receive.RTDEReceiveInterface(host)
# gripper
rtde_io = rtde_io.RTDEIOInterface(host)

if __name__ == "__main__":
    
    #p[1] += 0.01         #x tengely fix (előre, hátra)
    #p[2] -= 0.01         #y tengely fix (fel, le)
    #p[3] -= 0.1
    #p[4] += 0.1
    #p[5] += 0.1
    #p[6] += 0.1
    
    velocity = 1
    acceleration = 1

    #TARGET = [Base, Shoulder, Elbow, Wrist1, Wrist2, Wrist3]
    target1 = [-0.015, -0.935, 0.85, -1.5, 4.75, 1.6]
    target3 = [3, -0.935, 1.2, -1.85, 4.75, 1.6]
    
    rtde_io.setStandardDigitalOut(0, False)
    
    rtde_c.moveJ(target1, velocity, acceleration)
    
    subprocess.call(["python", "fp_elinditas.py"])
    
    p = rtde_r.getActualTCPPose()
    #print(f"pose {p}")
    target2 = p
    target2[2] -= 0.1
    
    rtde_c.moveL(target2, velocity, acceleration)
    
    rtde_io.setStandardDigitalOut(0, True)
    
    rtde_c.moveJ(target1, velocity, acceleration)
    rtde_c.moveJ(target3, velocity, acceleration)
    
    p = rtde_r.getActualTCPPose()
    #print(f"pose {p}")
    target4 = p
    target4[2] -= 0.06
    
    rtde_c.moveL(target4, velocity, acceleration)
    rtde_io.setStandardDigitalOut(0, False)
    
    rtde_c.stopScript()