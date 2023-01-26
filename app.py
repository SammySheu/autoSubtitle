from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import datetime
import os
from mysql_init.mysql_config import setUpDB, addUser, addVideo
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity
)
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024     # 512 MB
app.config['ALLOWED_EXTENSIONS'] = ['.mp4']
app.config['JWT_SECRET_KEY'] = 'secret'

jwt = JWTManager(app)
User, Video = setUpDB(app)

@app.route('/', methods=['GET'])
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    videos = []
    for file in files:
        if os.path.splitext(file)[1] in app.config['ALLOWED_EXTENSIONS']:
            videos.append(file)
    print(videos)
    return render_template('upload_page.html', videos = videos)

@app.route('/register', methods=['POST'])
def register():
    user = User(   
        user_email = request.form['email'],
        user_password = request.form['password'],
    )
    searchEmail = User.query.filter_by(user_email=request.form['email']).first()
    if not searchEmail:                     # if email doesn't exist, build one
        addUser(app, user)
        return 'Register successfully'
    else:
        return 'Email already exists'

@app.route('/login', methods=['POST'])   
def loginPost():
    searchData = User.query.filter_by(user_email=request.form['email']).first()
    if searchData:
        if searchData.user_password == request.form['password']:
            currentUser = {
                'user_email':searchData.user_email,
                'user_password':searchData.user_password
            }
            access_token = create_access_token(identity=json.dumps(currentUser), expires_delta=datetime.timedelta(minutes=15))
            return jsonify(access_token=access_token), 201
        else:
            return 'Incorrect password\n', 200
    else:
        return 'No such user was found\n', 200

@app.route('/upload-video', methods=['POST'])
def upload():
    file = request.files['file_from_user']
    
    if file:                # Make sure there is file included in request.file
        extension = file.filename.split('.')[1]
        if extension == 'mp4':
            time_now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S_')
            file_name = secure_filename(file.filename)
            rel_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                time_now + file_name
            )
            abs_path = os.path.join(os.getcwd() ,rel_path)
            file.save(rel_path)
            video = Video(
                video_name  = file_name,
                video_url   = abs_path,
                video_owner = 3,
            )
            addVideo(app, video)
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
    # app.run(debug=True)
    app.run(host='0.0.0.0',port=5555, debug=True)