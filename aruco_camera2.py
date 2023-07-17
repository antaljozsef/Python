import cv2
from cv2 import aruco
import numpy as np

# Sakktábla mérete
chessboard_size = (9, 6)  # Belső sarkok száma (oszlopok, sorok)

# Kamera és marker távolság beállítása milliméterben
camera_to_marker_distance_mm = 400  # 40 cm = 400 mm

# Kamera kalibrációhoz szükséges változók
object_points = []  # Valós koordináták (0, 0, 0), (1, 0, 0), ..., (8, 5, 0)
image_points = []  # Képen mért sarkok koordinátái

cap = cv2.VideoCapture(0)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    parameters = aruco.DetectorParameters_create()
    parameters.minMarkerPerimeterRate = 0.05
    parameters.minCornerDistanceRate = 0.05
    
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow('ArUco Detection', frame_markers)
    
    if ids is not None and len(ids) > 1:
        all_ids = []
        all_corners = []
        for i in range(len(ids)):
            marker_width = abs(corners[i][0][0][0] - corners[i][0][1][0])
            marker_height = abs(corners[i][0][0][1] - corners[i][0][3][1])
            
            # Szélesség és magasság átszámítása mm-re
            marker_width_mm = marker_width * camera_to_marker_distance_mm / frame.shape[1]
            marker_height_mm = marker_height * camera_to_marker_distance_mm / frame.shape[0]
            
            print("ID:", ids[i])
            print("Marker szélessége:", marker_width_mm, "mm")
            print("Marker magassága:", marker_height_mm, "mm")

            all_ids.append(ids[i])
            all_corners.append(corners[i])
    
        # Azonosítók és sarkok összeállítása numpy tömbökké
        all_ids = np.array(all_ids)
        all_corners = np.array(all_corners)

        # Több marker szélesség és magasság meghatározása
        marker_widths = np.abs(all_corners[:, 0, 0, 0] - all_corners[:, 0, 1, 0]) * camera_to_marker_distance_mm / frame.shape[1]
        marker_heights = np.abs(all_corners[:, 0, 0, 1] - all_corners[:, 0, 3, 1]) * camera_to_marker_distance_mm / frame.shape[0]

        for i in range(len(all_ids)):
            # Az adott marker szélességének és magasságának kiíratása
            print("ID:", all_ids[i])
            print("Marker szélessége:", marker_widths[i], "mm")
            print("Marker magassága:", marker_heights[i], "mm")

            # Sakktábla sarkok koordinátáinak detektálása
            ret, chessboard_corners = cv2.findChessboardCorners(gray, chessboard_size, None)
            
            if ret:
                object_points.append(np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32))
                object_points[-1][:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
                image_points.append(chessboard_corners)

        print()  # Üres sor a jobb olvashatóságért
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Kamera kalibráció
ret, camera_matrix, distortion_coefficients, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, gray.shape[::-1], None, None)

# Elmenti a kamera kalibrációs eredményeket
np.savez("camera_calibration.npz", camera_matrix=camera_matrix, distortion_coefficients=distortion_coefficients)
