import cv2
from cv2 import aruco
from flask import Flask, render_template, Response

app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture(0)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    marker_length = 0.02  # Length of the markers in meters
    pixel_to_mm_conversion = 10  # Example conversion factor: 10 pixels = 1 millimeter

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            marker_size = aruco.estimatePoseSingleMarkers(corners, marker_length, camera_matrix, distortion_coefficients)
            for i in range(len(ids)):
                rvec, tvec = marker_size[0][i, 0, :3], marker_size[1][i, 0, :3]
                marker_width = abs(corners[i][0][0][0] - corners[i][0][1][0])  # Width of the marker in pixels
                marker_height = abs(corners[i][0][0][1] - corners[i][0][2][1])  # Height of the marker in pixels
                marker_width_mm = marker_width * pixel_to_mm_conversion  # Width of the marker in millimeters
                marker_height_mm = marker_height * pixel_to_mm_conversion  # Height of the marker in millimeters

                cv2.putText(frame, f"Width: {marker_width_mm:.2f} mm", (int(corners[i][0][1][0]), int(corners[i][0][1][1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, f"Height: {marker_height_mm:.2f} mm", (int(corners[i][0][2][0]), int(corners[i][0][2][1]) + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
