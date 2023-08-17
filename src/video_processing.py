import cv2
import subprocess
from object_detection import detect_objects
import os
import shutil
from flask import jsonify

# global variable to store progress
progress = 0
def get_progress():
    global progress
    return progress

def process_video(input_video_path, output_video_path):

    global progress
    progress = 0

    # temp frame directory
    frames_dir = "frames/"
    annotated_frames_dir = "annotated_frames/"
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(annotated_frames_dir, exist_ok=True)

    # extract frames using FFmpeg
    print('extracting frames')
    extract_command = f"ffmpeg -i {input_video_path} -vf fps=30 {frames_dir}frame_%03d.jpg"
    subprocess.call(extract_command, shell=True)

    # transcode into multiple qualities
    qualities = [(1280, 720), (640, 360)]  # example resolutions (HD and SD)
    for width, height in qualities:
        transcoded_path = os.path.join(frames_dir, f"{width}x{height}")
        os.makedirs(transcoded_path, exist_ok=True)
        transcoding_command = f"ffmpeg -i {frames_dir}frame_%03d.jpg -vf scale={width}:{height} {transcoded_path}/frame_%03d.jpg"
        subprocess.call(transcoding_command, shell=True)

    # annotate frames with bounding boxes for each quality level
    for width, height in qualities:
        transcoded_path = os.path.join(frames_dir, f"{width}x{height}")
        annotated_path = os.path.join(annotated_frames_dir, f"{width}x{height}")
        os.makedirs(annotated_path, exist_ok=True)
        counter = 0
        total_frames = len(os.listdir(transcoded_path))
        for frame_file in os.listdir(transcoded_path):
            frame_path = os.path.join(transcoded_path, frame_file)
            frame = cv2.imread(frame_path)
            print(f"processing frame {counter} of  {total_frames}")
            # track progress and update the global variable
            progress = (counter / total_frames) * 100
            counter += 1
            detected_objects = detect_objects(frame)
            for obj in detected_objects:
                label, confidence, box = obj
                if confidence > 0.75:  # only include confident detections
                    x_min, y_min, x_max, y_max = map(int, box)  # convert to integer
                    x, y, w, h = x_min, y_min, x_max - x_min, y_max - y_min
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.putText(frame, f"{label}: {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            annotated_frame_path = os.path.join(annotated_path, frame_file)
            cv2.imwrite(annotated_frame_path, frame)


    # reassemble annotated frames into HD and SD video for HLS
    for width, height in qualities:
        annotated_path = os.path.join(annotated_frames_dir, f"{width}x{height}")
        reassemble_command = (
            f"ffmpeg -i {annotated_path}/frame_%03d.jpg -vcodec libx264 -crf 25 "
            f"-b:v 1024k -strict experimental -f hls {annotated_path}/index.m3u8"
            )
        subprocess.call(reassemble_command, shell=True)

    print('video processing complete')
    # reset progress to 100% at the end
    progress = 100

# master playlist defintion
def create_master_playlist(hd_playlist, sd_playlist, master_playlist_path):
    with open(master_playlist_path, 'w') as master_file:
        master_file.write("#EXTM3U\\n")
        master_file.write(f"#EXT-X-STREAM-INF:BANDWIDTH=8000000,RESOLUTION=1280x720\\n{hd_playlist}\\n")
        master_file.write(f"#EXT-X-STREAM-INF:BANDWIDTH=4000000,RESOLUTION=640x360\\n{sd_playlist}\\n")

# paths for frames and playlists
annotated_frames_dir = "annotated_frames/"
master_playlist_path = os.path.join(annotated_frames_dir, 'master_playlist.m3u8')
hd_playlist = os.path.join(annotated_frames_dir, '1280x720', 'index.m3u8')
sd_playlist = os.path.join(annotated_frames_dir, '640x360', 'index.m3u8')

create_master_playlist(hd_playlist, sd_playlist, master_playlist_path)





