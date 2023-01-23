from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024     # 16 MB


@app.route('/', methods=['GET'])
def index():
    return render_template('upload_page.html')

@app.route('/upload-video', methods=['POST'])
def upload():
    file = request.files['file_from_user']
    if file:                # Make sure there is file included in request.file
        time_now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S_')
        file.save(os.path.join(
            app.config['UPLOAD_DIRECTORY'],
            time_now + secure_filename(file.filename)
        ))
        return 'Upload successfully'
    return 'There is no any files'

if __name__ == "__main__":
    app.run(debug=True)