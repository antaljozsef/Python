# Robot Vezérlő Program

Ez a program egy robotkar irányítására szolgál, ArUco marker detekció alkalmazásával. Három fő folyamatból áll, melyek egyszerre futnak:

1. **Motorvezérlési Folyamat (`control_motor`):** Ez a folyamat inicializálja és vezérli a motort a `ticcmd` parancssori eszközzel. A motor állandóan be van kapcsolva, amíg a folyamatot nem állítják le.

2. **ArUco Jelölődetekciós Folyamat (`detect_and_display_aruco`):** Ez a folyamat videót vesz fel egy kameráról, detektálja az ArUco markereket, kiszámolja a pozícióikat, majd a megfelelő információkat továbbítja a robotvezérlő folyamatnak.

3. **Robotvezérlési Folyamat (`move_robot_arm`):** Ez a folyamat a Real-Time Data Exchange (RTDE) protokollt használva irányítja a robotkart. Megkapja az ArUco marker pozícióját, mozgatja a robotkart, és végrehajt a darab megfogását.

## Követelmények
- Python 3
- OpenCV (`cv2`)
- Numpy
- RTDE Control
- RTDE Receive
- RTDE IO
- Keyboard

## Használat
1. Telepítsd a szükséges Python csomagokat: `pip install opencv-python numpy rtde-control rtde-receive rtde-io keyboard`.
2. Indítsd be a robotkart.
3. Csatlakoz úgyan arra a wifi hálózatra, amelyikre a robot is csatlakozik.
4. Csatlakoztasd a kamerást és a fútószalagot a számítogéphez.
5. Indítsd el a programot: `python multiprocessing.py`.

Megjegyzés: Győződj meg róla, hogy a szükséges függőségek telepítve vannak.

## Hozzájáruló
- Antal József