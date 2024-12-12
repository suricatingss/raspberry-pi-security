from flask import Flask, Response, request, render_template_string
import cv2

app = Flask(__name__)


# Function to generate video frames
def generate_frames(camera_index):
    cap = cv2.VideoCapture(camera_index)  # Open the specified camera
    while True:
        success, frame = cap.read()  # Read the frame
        if not success:
            break

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in the appropriate format for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Stream the frame


@app.route('/video_feed')
def video_feed():
    camera_index = request.args.get('camera', default=0, type=int)  # Get camera index from query params
    response = Response(generate_frames(camera_index),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    response.headers["X-Video-Height"] = '720'
    response.headers["X-Video-Width"] = '1280'
    return response

@app.route('/')
def index():
    # Simple HTML form to select camera index
    return render_template_string('''
        <html>
            <head>
                <title>Select Camera</title>
            </head>
            <body>
                <h1>Select Camera</h1>
                <form action="/video_feed" method="get">
                    <label for="camera">Camera Index:</label>
                    <input type="number" id="camera" name="camera" value="0" min="0">
                    <input type="submit" value="Start Stream">
                </form>
                <h2>Live Stream</h2>
                <img id="liveStream" src="/video_feed?camera=0" style="width: 100%; height: auto;" />
            </body>
        </html>
        
        <style>
        body {
        background-color: #131313;
        color: white;
        }
        
        </style>
    ''')


def run(): app.run(host='127.0.0.1', port=5000) # começar a correr a webapp

if __name__ == "__main__": run()

