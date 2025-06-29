import os
import json
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
WALLPAPER_FOLDER = 'static/images'
SETTINGS_FILE = 'user_settings.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['WALLPAPER_FOLDER'] = WALLPAPER_FOLDER

@app.route('/')
def index():
    albums = [name for name in os.listdir(UPLOAD_FOLDER)
              if os.path.isdir(os.path.join(UPLOAD_FOLDER, name))]
    return render_template('index.html', albums=albums)

@app.route('/album/<album_name>')
def album(album_name):
    album_path = os.path.join(UPLOAD_FOLDER, album_name)
    if not os.path.exists(album_path):
        return "Альбом не найден", 404
    photos = [photo for photo in os.listdir(album_path)
              if photo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('album.html', album=album_name, photos=photos)

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

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    message = ''
    settings_data = {}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings_data = json.load(f)

    if request.method == 'POST':
        # Загрузка обоев
        file = request.files.get('wallpaper')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            wallpaper_path = os.path.join(WALLPAPER_FOLDER, filename)
            if not os.path.exists(WALLPAPER_FOLDER):
                os.makedirs(WALLPAPER_FOLDER)
            file.save(wallpaper_path)
            settings_data['wallpaper'] = filename
            message = 'Обои успешно загружены!'

        # Цвет текста
        text_color = request.form.get('text_color', '').strip()
        if text_color and len(text_color) == 6 and all(c in '0123456789abcdefABCDEF' for c in text_color):
            settings_data['text_color'] = text_color
        else:
            settings_data['text_color'] = settings_data.get('text_color', '000000')

        # Размер шрифта
        try:
            font_size = int(request.form.get('font_size', 24))
            if 10 <= font_size <= 72:
                settings_data['font_size'] = font_size
            else:
                settings_data['font_size'] = 24
        except ValueError:
            settings_data['font_size'] = 24

        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings_data, f)

        if not message:
            message = 'Настройки успешно сохранены!'

    return render_template('settings.html',
                           message=message,
                           text_color=settings_data.get('text_color', ''),
                           font_size=settings_data.get('font_size', 24),
                           wallpaper=settings_data.get('wallpaper'))

@app.context_processor
def inject_settings():
    settings_data = {}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings_data = json.load(f)
    wallpaper_url = None
    if 'wallpaper' in settings_data:
        wallpaper_url = url_for('static', filename='images/' + settings_data['wallpaper'])
    return dict(
        wallpaper_url=wallpaper_url,
        text_color=settings_data.get('text_color', '000000'),
        font_size=settings_data.get('font_size', 24)
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
