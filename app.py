from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def gallery():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        file = request.files['photo']
        if file.filename != '':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('gallery'))

import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Список папок (альбомов) в uploads
    albums = [name for name in os.listdir(UPLOAD_FOLDER)
              if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]
    return render_template('index.html', albums=albums)

@app.route('/album/<album_name>')
def album(album_name):
    album_path = os.path.join(UPLOAD_FOLDER, album_name)
    if not os.path.exists(album_path):
        return "Альбом не найден", 404
    photos = os.listdir(album_path)
    photos = [photo for photo in photos if photo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('album.html', album=album_name, photos=photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    albums = [name for name in os.listdir(UPLOAD_FOLDER)
              if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]
    if request.method == 'POST':
        album = request.form.get('album')
        file = request.files.get('photo')
        if album and file and file.filename != '':
            album_path = os.path.join(UPLOAD_FOLDER, album)
            if not os.path.exists(album_path):
                os.makedirs(album_path)
            file.save(os.path.join(album_path, file.filename))
            return redirect(url_for('album', album_name=album))
    return render_template('upload.html', albums=albums)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    albums = [name for name in os.listdir(UPLOAD_FOLDER)
              if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]
    if request.method == 'POST':
        # Получаем имя выбранного альбома и нового альбома
        album = request.form.get('album')
        new_album = request.form.get('new_album').strip()

        # Если введено имя нового альбома, используем его
        if new_album:
            album = new_album

        file = request.files.get('photo')
        if album and file and file.filename != '':
            album_path = os.path.join(UPLOAD_FOLDER, album)
            if not os.path.exists(album_path):
                os.makedirs(album_path)  # Создаем новую папку-альбом
            file.save(os.path.join(album_path, file.filename))
            return redirect(url_for('album', album_name=album))
    return render_template('upload.html', albums=albums)
