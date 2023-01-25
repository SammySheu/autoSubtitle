from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024     # 16 MB
app.config['ALLOWED_EXTENSIONS'] = ['.mp4']


@app.route('/', methods=['GET'])
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    videos = []
    for file in files:
        if os.path.splitext(file)[1] in app.config['ALLOWED_EXTENSIONS']:
            videos.append(file)
    print(videos)
    return render_template('upload_page.html', videos = videos)

@app.route('/upload-video', methods=['POST'])
def upload():
    file = request.files['file_from_user']
    if file:                # Make sure there is file included in request.file
        extension = file.filename.split('.')[1]
        if extension == 'mp4':
            time_now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S_')
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'],
                time_now + secure_filename(file.filename)
            ))
            return 'Upload successfully'
        else:
            return 'Only mp4 file is available'
    return 'There is no any files'

@app.route('/serve-file/<filename>', methods=['GET'])
def display_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/add-subtitles', methods=['POST'])
def add_subtitles():
    video_name = '2023-01-26_00:49:17_etkl8-wo7lj'
    os.system(f'autosub -S zh-TW -D zh-TW -o ./srt_file/test.srt ./uploads/{video_name}.mp4')
    os.system(f"ffmpeg -i ./uploads/{video_name}.mp4 -vf 'subtitles=./srt_file/test.srt' ./uploads/outputWithSubtitle.mp4")
    return 'Successfully add subtitles'
if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', debug=True)