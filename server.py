from flask import Flask, request, redirect, url_for, render_template, flash
import os
import zipfile
import shutil
import tensorflow as tf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MODEL_SERVING'] = 'model_serving'
app.secret_key = 'supersecretkey'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB


def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.zip'):
            zip_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(zip_path)
            model_name = os.path.splitext(file.filename)[0]
            extract_path = os.path.join(app.config['MODEL_SERVING'], f'saved_model_{model_name}')
            os.makedirs(extract_path, exist_ok=True)
            unzip_file(zip_path, extract_path)
            flash(f"File for '{model_name}' model successfully uploaded and saved")
            return redirect(url_for('upload_file'))
        else:
            flash('Allowed file type is zip')
            return redirect(request.url)
    return render_template('index.html')


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['MODEL_SERVING'], exist_ok=True)
    app.run(debug=True)
