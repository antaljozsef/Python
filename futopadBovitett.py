import subprocess
import time


def ticcmd(*args):
    return subprocess.check_output(["ticcmd"] + list(args))


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
