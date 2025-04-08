from flask import Flask, render_template, request, redirect, url_for
import os
from utils import get_all_filenames, compute_tf_idf_for_file
from mylog import log
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Главная страница со списком файлов
@app.route('/')
def index():
    filenames = get_all_filenames(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', filenames=filenames)

# Загрузка файла (без обработки)
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and file.filename.endswith('.txt'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
    return redirect(url_for('index'))

# Удаление всех файлов
@app.route('/delete_all')
def delete_all():
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(path):
            os.remove(path)
    return redirect(url_for('index'))

# Анализ конкретного файла
@app.route('/analyze/<filename>')
def analyze(filename):
    folder = app.config['UPLOAD_FOLDER']
    results = compute_tf_idf_for_file(filename, folder)

    # читаем исходный текст файла
    filepath = os.path.join(folder, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        original_text = f.read()

    return render_template(
        'results.html',
        words=results,
        filename=filename,
        original_text=original_text
    )

@app.route('/copy_test_files')
def copy_test_files():
    test_folder = os.path.join(app.root_path, 'test')
    upload_folder = app.config['UPLOAD_FOLDER']

    if not os.path.exists(test_folder):
        return "Папка test/ не найдена", 404

    for filename in os.listdir(test_folder):
        if filename.endswith('.txt'):
            src = os.path.join(test_folder, filename)
            dst = os.path.join(upload_folder, filename)
            shutil.copy(src, dst)

    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5555, debug=True)

