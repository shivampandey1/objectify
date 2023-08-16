from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response
from werkzeug.utils import secure_filename
import os
from video_processing import process_video
from pathlib import Path
import mimetypes

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # check uploads directory exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Add this line
            
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)

            # process video
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], "processed_" + filename)
            process_video(input_path, output_path)

            return redirect(url_for('view_video', filename="processed_" + filename))

    return render_template('index.html')


@app.route('/view/<filename>')
def view_video(filename):
    return render_template('view.html', filename=filename)

@app.route('/uploads/<filename>')
def serve_video(filename):
    print('----------serve_video----------')
    print("serving file:", filename)
    print("configured upload relative folder:", app.config['UPLOAD_FOLDER'])
    absolute_upload_folder = Path(app.config['UPLOAD_FOLDER']).resolve()
    print("configured upload absolute folder:", absolute_upload_folder)
    absolute_file_path = absolute_upload_folder / filename
    print("requested file absolute path:", absolute_file_path)
    file_exists = absolute_file_path.is_file()
    print("file exists:", file_exists)
    print('-------------------------------')

    # check if the requested file exists
    if absolute_file_path.is_file():
        # file MIME type
        mime_type, _ = mimetypes.guess_type(absolute_file_path)

        # read the file
        with open(absolute_file_path, 'rb') as file:
            file_content = file.read()

        # create a response with the file content + headers
        response = Response(file_content, content_type=mime_type)
        response.headers['Content-Disposition'] = f'inline; filename={filename}'
        return response
    else:
        return f"File not found at path: {absolute_file_path}", 404

if __name__ == "__main__":
    app.run(debug=True)

