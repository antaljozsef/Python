from flask import Flask, render_template, Response, jsonify
import cv2
from cv2 import aruco
import numpy as np

app = Flask(__name__)

class Marker:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height

def generate_frames():
    cap = cv2.VideoCapture(0)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    marker_length = 0.02  # Marker length in meters
    marker_width_mm = 10  # Marker width in millimeters
    marker_height_mm = 20  # Marker height in millimeters

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        markers = []  # List to store marker data

        if ids is not None:
            for i in range(len(ids)):
                marker = Marker(ids[i][0], marker_width_mm, marker_height_mm)
                markers.append(marker)
                # Kiírjuk a marker azonosítóját a képre
                cv2.putText(frame, str(marker.id), tuple(corners[i][0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame', direct_passthrough=True)

@app.route('/marker_data')
def marker_data():
    markers = get_markers()
    marker_data = [{'id': marker.id, 'width': marker.width, 'height': marker.height} for marker in markers]
    return jsonify(markers=marker_data)

def get_markers():
    markers = [
        Marker(1, 0, 0),
        Marker(2, 0, 0),
        Marker(3, 0, 0),
        Marker(4, 0, 0),
        Marker(5, 0, 0),
        Marker(6, 0, 0),
        Marker(7, 0, 0),
        Marker(8, 0, 0),
        Marker(9, 0, 0),
        Marker(10, 0, 0),
        Marker(11, 0, 0),
        Marker(12, 0, 0),
    ]
    
    return markers

def get_marker_dimensions(marker_id):
    markers = get_markers()
    
    for marker in markers:
        if marker.id == marker_id:
            return marker.width, marker.height
    
    return None, None

if __name__ == '__main__':
    app.run(debug=True)
