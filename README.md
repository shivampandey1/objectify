# Objectify

Objectify is a web application designed to process video files by performing object detection and generating adaptive HLS (HTTP Live Streaming) streams with multiple quality levels.

## Features

- **Object Detection**: Utilizes a Convolutional Neural Network (CNN) to identify and label objects within each frame of a video.
- **Quality Transcoding**: Transcodes each frame into multiple resolutions to enable adaptive streaming.
- **HLS Streaming**: Creates HLS master playlists and allows users to view videos in different resolutions according to their internet connection.
- **Progress Tracking**: Provides a visual indication of the processing progress to the user.

## Technical Breakdown

### 1. **Video Processing**:
  - **Frame Extraction**: Extracts frames from the input video using FFmpeg.
  - **Quality Transcoding**: Transcodes frames into HD and SD resolutions.
  - **Object Detection**: Uses a pre-trained CNN to detect objects in each frame and annotate them with bounding boxes.
  - **Frame Reassembly**: Combines annotated frames into HD and SD video streams.
  - **HLS Master Playlist**: Generates an HLS master playlist for adaptive streaming.

### 2. **Web Interface**:
  - **File Upload**: Allows users to upload MP4 video files for processing.
  - **Progress Bar**: Shows a real-time progress bar to indicate the processing status.
  - **Video Playback**: Enables users to view the processed video with selectable resolutions through an HLS player.
  - **Download Link**: Offers a download link for the processed video.

### 3. **Directory Management**:
  - **Temporary Storage**: Manages directories for storing frames, annotated frames, and uploaded videos.
  - **Clean-Up Script**: Includes a script to wipe the contents of temporary directories.

## Tools and Technologies

- **Python**: Main programming language for backend processing.
- **Flask**: Web framework for handling HTTP requests and serving web pages.
- **FFmpeg**: Used for video frame extraction and transcoding.
- **OpenCV**: Utilized for image processing and object detection.
- **Tailwind CSS**: Applies styling to the frontend interface.
- **HLS.js**: JavaScript library to handle HLS playback in the browser

---
## How to Use

### 1. **Installation**:
   Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/your-username/objectify.git
   cd objectify
   ```

### 2. **Install Dependencies**:
   Install the required packages using the following command:
   ```bash
   pip install -r requirements.txt
   ```

### 3. **Run the Application**:
   Start the Flask server:
   ```bash
   python src/web_interface.py
   ```

### 4. **Access the Web Interface**:
   Open your web browser and navigate to `http://127.0.0.1:5000/`.

### 5. **Upload and Process Video**:
   - Click the "Upload" button to select an MP4 video file.
   - The application will process the video, showing a progress bar.
   - Once processing is complete, you can view or download the processed video in different resolutions.

### 6. **Clean Temporary Files** (Optional):
   Run the provided script to delete temporary files:
   ```bash
   python src/clear_directories.py
   ```

## Dependencies

Objectify relies on several libraries and tools. The main dependencies are:

- **Python**: 3.6 or higher
- **Flask**: Web framework
- **FFmpeg**: Video processing tool
- **OpenCV**: Computer vision library
- **Tailwind CSS**: Frontend styling framework
- **HLS.js**: HLS playback in browsers

All Python dependencies can be installed using the provided `requirements.txt` file.

For FFmpeg, needs to be installed seperately. Instructions for installation can be found on the [official FFmpeg website](https://ffmpeg.org/download.html).
