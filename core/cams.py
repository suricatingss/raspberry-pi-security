import subprocess, cv2, os, time, sys
from core import schema
import main
available_cameras = []
recording_cams = {}

def getStringTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# noinspection PyUnreachableCode

def intrustion_procedure():
    target_dir = getFolderDir(True)
    now_folder = f'{target_dir}/{getStringTime()}'
    os.makedirs(now_folder, exist_ok=True)
    available_cams = find_cameras()
    for camera in available_cams:
        take_pic(camera,True,now_folder)

def find_cameras():
    #available_cameras = []
    global available_cameras
    for index in range(10):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():  # Check if the camera is available
            available_cameras.append(index)
            cap.release()  # Release the camera after checking
        else: continue
    return available_cameras



def getFolderDir(triggered):
    if triggered: destFolder = "intrusions"
    else: destFolder = "normal"
    # Obter o caminho atual (core*/985cams.py
    current_dir = os.path.dirname(__file__)

    # Juntar caminhos. Um acima, e depois a pasta
    footage_dir = os.path.join(current_dir, '..', 'footage', destFolder)

    # Make sure it's an absolute path (optional but recommended)
    return os.path.abspath(footage_dir)

    #image_path = os.path.join(footage_dir, 'captured_image.jpg')
    #print(f"Image will be saved to: {image_path}")


def take_pic(id = 0, trigger = False, customDir = None):
    cap = cv2.VideoCapture(id)
    ret, frame = cap.read()
    if ret:
        if customDir is None: output = os.path.join(getFolderDir(trigger), f'{getStringTime()}-{id}.jpg')
        else: output = os.path.join(customDir, f'{getStringTime()}-{id}.jpg')
        cv2.imwrite(output, frame)
    cap.release()

def record_video(id = 0, duration = 0, trigger = False):
    cap = cv2.VideoCapture(id)
    footage_dir = getFolderDir(trigger)  # Get the footage directory
    video_path = os.path.join(footage_dir, f'{getStringTime()}.mp4')  # Define the output video path

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
    fps = 30.0  # Frames per second
    frame_size = (int(cap.get(3)), int(cap.get(4)))  # Get the width and height of the frame

    # Create VideoWriter object to save the video
    out = cv2.VideoWriter(video_path, fourcc, fps, frame_size)

    # print(f"Recording video for {duration_seconds} seconds...")

    # Start recording and track time
    start_time = time.time()
    recording_cams[id] = True

    # enquanto 'cap' estiver aberto

    while cap.isOpened() and (start_time - time.time() < duration or duration == 0)\
            and recording_cams[id] == True:
        ret, frame = cap.read()
        if ret: out.write(frame) # Adicionar frame ao vídeo
        else: break

    # Release everything once done
    cap.release()
    out.release()

def stop_recording(id = 0): recording_cams[id] = False

for camera in available_cameras: recording_cams[camera] = False


if __name__ == "__main__": # Acionado pelo PHP
    action = int(sys.argv[1])
    camId = int(sys.argv[2])


