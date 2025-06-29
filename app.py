import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    albums = [name for name in os.listdir(UPLOAD_FOLDER)
              if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]
    if request.method == 'POST':
        album = request.form.get('album')
        new_album = request.form.get('new_album', '').strip()

        # Если введено имя нового альбома, используем его
        if new_album:
            album = new_album

        file = request.files.get('photo')
        if album and file and file.filename != '':
            album_path = os.path.join(UPLOAD_FOLDER, album)
            if not os.path.exists(album_path):
                os.makedirs(album_path)
            filename = secure_filename(file.filename)
            file.save(os.path.join(album_path, filename))
            return redirect(url_for('album', album_name=album))
    return render_template('upload.html', albums=albums)
