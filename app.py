from flask import Flask, render_template, request, send_from_directory, jsonify, redirect
from werkzeug.utils import secure_filename
import datetime
import os
from mysql_init.mysql_config import setUpDB, addUser, addVideo
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    unset_jwt_cookies,
    set_access_cookies
)
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024     # 512 MB
app.config['ALLOWED_EXTENSIONS'] = ['.mp4']
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config['JWT_SECRET_KEY'] = 'secret'
app.config["JWT_COOKIE_SECURE"] = False


jwt = JWTManager(app)
User, Video = setUpDB(app)

@app.route('/', methods=['GET'])
@jwt_required()
def index():
    jwt_certificated_data = get_jwt_identity()
    jwt_certificated_data = json.loads(jwt_certificated_data)
    userVideos = Video.query.filter_by(video_owner=jwt_certificated_data['user_id'])
    videos = []
    for row in userVideos:
        print(row.video_name)
        videos.append(row.video_name)
    # files = os.listdir(app.config['UPLOAD_FOLDER'])
    # videos = []
    # for file in files:
    #     if os.path.splitext(file)[1] in app.config['ALLOWED_EXTENSIONS']:
    #         videos.append(file)

    # print(videos)
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

@app.route('/login', methods=['GET'])
def loginGet():
    return render_template('login_page.html')

@app.route('/login', methods=['POST'])   
def loginPost():
    data = request.get_json()
    if (not data['user_email']) or (not data['user_password']):
        return jsonify(msg = 'Missing information')
    searchData = User.query.filter_by(user_email=data['user_email']).first()
    if searchData:
        if searchData.user_password == data['user_password']:
            currentUser = {
                'user_id': searchData.user_id
                # 'user_email':searchData.user_email,
                # 'user_password':searchData.user_password
            }
            response = jsonify({"msg": "login successful"})
            access_token = create_access_token(identity=json.dumps(currentUser), expires_delta=datetime.timedelta(minutes=15))
            set_access_cookies(response, access_token)
            return response
        else:
            return jsonify(msg = 'Incorrect password\n'), 200
    else:
        return jsonify(msg = 'No such user was found\n'), 200

@app.route('/upload-video', methods=['POST'])
@jwt_required()
def upload():
    file = request.files['file_from_user']
    
    if file:                # Make sure there is file included in request.file
        extension = file.filename.split('.')[1]
        if extension == 'mp4':
            time_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_')
            file_name = time_now + secure_filename(file.filename)
            rel_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                file_name
            )
            abs_path = os.path.join(os.getcwd() ,rel_path)
            jwt_certificated_data = get_jwt_identity()
            jwt_certificated_data = json.loads(jwt_certificated_data)
            # print(jwt_certificated_data)
            # userInfo = User.query.filter_by(user_id=jwt_certificated_data['user_email']).first()
            file.save(rel_path)
            video = Video(
                video_name  = file_name,
                video_url   = abs_path,
                video_owner = jwt_certificated_data['user_id']
            )
            addVideo(app, video)
            return jsonify(msg = 'Upload successfully\n'), 200
        else:
            return 'Only mp4 file is available'
    return 'There is no any files'

@app.route('/serve-file/<filename>', methods=['GET'])
def display_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/add-subtitles', methods=['POST'])
@jwt_required()
def add_subtitles():
    print(json.loads(request.data))
    video_name = json.loads(request.data)
    os.system(f'autosub -S zh-TW -D zh-TW -o ./srt_file/{video_name}.srt ./uploads/{video_name}.mp4')
    os.system(f"ffmpeg -i ./uploads/{video_name}.mp4 -vf 'subtitles=./srt_file/{video_name}.srt' ./uploads/{video_name}_srt.mp4")
    return jsonify(msg = 'Successfully add subtitles')

@app.route("/logout", methods=["POST"])
# @jwt_required()
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0',port=5555, debug=True)