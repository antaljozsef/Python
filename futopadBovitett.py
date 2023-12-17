import subprocess
import time
import keyboard


def ticcmd(*args):
    return subprocess.check_output(["ticcmd"] + list(args))


# TIC motorvezérlő inicializálása
ticcmd("--exit-safe-start")

ticcmd("--velocity", "-40000000")

while True:
    # Motor bekapcsolása
    ticcmd("--energize")

    # start_time = time.time()

    #     current_time = time.time()
    #     elapsed_time = current_time - start_time

    #     if elapsed_time >= 1.8:

    if keyboard.is_pressed("space"):
        start_time = time.time()
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time < 1.8:
            break
