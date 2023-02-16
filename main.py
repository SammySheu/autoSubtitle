from module.app import app
from flask import redirect, url_for, send_file, send_from_directory
from controllers.user import user
from controllers.workshop import workshop

app.config['USER_FOLDER'] = 'userFiles/'
app.config['SRT_FOLDER'] = 'srtFiles/'
app.config['WORKSHOP_FOLDER'] = 'workshopFiles/'
app.config['ROOT_FOLDER'] = '../'
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024     # 512 MB
app.config['ALLOWED_EXTENSIONS'] = ['.mp4']

@app.route('/')
def index():
    return redirect( url_for('user.loginGet') )
 
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(workshop, url_prefix='/workshop')

@app.route('/serve-file/<fileDirectory>/<fileName>', methods=['GET'])
def display_files(fileDirectory, fileName):
    # filePath = fileDirectory + '/' + fileName
    return send_from_directory( f'../{fileDirectory}', fileName, as_attachment=True)

if __name__ == "__main__":
    # app.run(debug=True, port = 5555)
    app.run(host='0.0.0.0',port=5555, debug=True)