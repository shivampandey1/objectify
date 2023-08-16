import cv2
import subprocess
from object_detection import detect_objects
import os
import shutil

def process_video(input_video_path, output_video_path):
    # temp frame directory
    frames_dir = "frames/"
    annotated_frames_dir = "annotated_frames/"
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(annotated_frames_dir, exist_ok=True)

    # extract frames using FFmpeg
    print('extracting frames')
    extract_command = f"ffmpeg -i {input_video_path} -vf fps=30 {frames_dir}frame_%03d.jpg"
    subprocess.run(extract_command, shell=True)

    # process frames
    frame_files = sorted(os.listdir(frames_dir))
    total_frames = len(frame_files)
    counter=0
    for frame_file in frame_files:
        print(f"processing frame {counter} of  {total_frames}")
        counter+=1
        frame_path = os.path.join(frames_dir, frame_file)

        # object detection
        detected_objects = detect_objects(frame_path)

        # read frames with OpenCV
        frame = cv2.imread(frame_path)

        # annotate frames with bounding boxes, labels, confidence scores
        for detection in detected_objects:
            label, confidence, bbox = detection['label'], detection['confidence'], detection['bbox']
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(0, 255, 0), thickness=2)
            cv2.putText(frame, f"{label}: {confidence:.2f}%", (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # save the annotated frame
        annotated_frame_path = os.path.join(annotated_frames_dir, frame_file)
        cv2.imwrite(annotated_frame_path, frame)

    # reassemble frames
    print('reassembling video')
    reassemble_command = f"ffmpeg -framerate 30 -i {annotated_frames_dir}frame_%03d.jpg -c:v libx264 -pix_fmt yuv420p {output_video_path}"
    subprocess.run(reassemble_command, shell=True)

    # clean up temporary directories
    shutil.rmtree(frames_dir)
    shutil.rmtree(annotated_frames_dir)
    print('finished processing of video')
