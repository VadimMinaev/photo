import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Путь для хранения обоев
WALLPAPER_FOLDER = 'static/images'
app.config['WALLPAPER_FOLDER'] = WALLPAPER_FOLDER

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

# Страница настроек и загрузка обоев
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    message = ''
    if request.method == 'POST':
        file = request.files.get('wallpaper')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            wallpaper_path = os.path.join(WALLPAPER_FOLDER, filename)
            file.save(wallpaper_path)
            message = 'Обои успешно загружены!'
            # Сохраняем имя файла в сессии или в файл для использования в шаблонах
            with open('current_wallpaper.txt', 'w') as f:
                f.write(filename)
        else:
            message = 'Ошибка загрузки файла.'
    # Читаем текущие обои
    wallpaper_filename = None
    if os.path.exists('current_wallpaper.txt'):
        with open('current_wallpaper.txt', 'r') as f:
            wallpaper_filename = f.read().strip()
    return render_template('settings.html', message=message, wallpaper=wallpaper_filename)

# Добавим функцию для передачи текущих обоев в шаблоны
@app.context_processor
def inject_wallpaper():
    wallpaper_url = None
    if os.path.exists('current_wallpaper.txt'):
        with open('current_wallpaper.txt', 'r') as f:
            filename = f.read().strip()
            wallpaper_url = url_for('static', filename='images/' + filename)
    return dict(wallpaper_url=wallpaper_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
