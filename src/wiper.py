import shutil
import os

def delete_directory_contents(directory_path):
    # Check if the directory exists
    if os.path.exists(directory_path):
        # Delete all contents of the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the annotated_frames and frames directories
annotated_frames_path = os.path.join(current_directory, '..', 'annotated_frames')
frames_path = os.path.join(current_directory, '..', 'frames')

# Delete the contents of the annotated_frames and frames directories
delete_directory_contents(annotated_frames_path)
delete_directory_contents(frames_path)

print("Contents of annotated_frames and frames have been deleted.")
