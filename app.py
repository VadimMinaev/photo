import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Главная - список альбомов
@app.route('/')
def index():
    albums = [name for name in os.listdir(UPLOAD_FOLDER)
              if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]
    return render_template('index.html', albums=albums)

# Просмотр фото в альбоме
@app.route('/album/<album_name>')
def album(album_name):
    album_path = os.path.join(UPLOAD_FOLDER, album_name)
    if not os.path.exists(album_path):
        return "Альбом не найден", 404
    photos = [photo for photo in os.listdir(album_path)
              if photo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('album.html', album=album_name, photos=photos)

# Загрузка фото с возможностью создания нового альбома
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    albums = [name for name in os.listdir(UPLOAD_FOLDER)
              if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]
    if request.method == 'POST':
        album = request.form.get('album')
        new_album = request.form.get('new_album', '').strip()

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


if __name__ == '__main__':
    # Запуск с доступом из локальной сети
    app.run(host='0.0.0.0', port=5000, debug=True)
