import warnings
warnings.filterwarnings("ignore", message="Unsupported Windows version*", category=UserWarning)
from flask import Flask, flash, request, render_template
import os
import cv2
from rembg import remove
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
def proccessImage(filename, operation):
    img = cv2.imread(f'{UPLOAD_FOLDER}/{filename}')
    match operation:
        case "cgray":
            imgProccessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFileName = f'static/{filename}'
            cv2.imwrite(newFileName, imgProccessed)
            return newFileName
        case "cpng":
            newFileName = f'static/{filename.split(".")[0]}.png'
            cv2.imwrite(newFileName, img)
            return newFileName
        case "cwebp":
            newFileName = f'static/{filename.split(".")[0]}.webp'
            cv2.imwrite(newFileName, img)
            return newFileName
        case "cjpg":
            newFileName = f'static/{filename.split(".")[0]}.jpg'
            cv2.imwrite(newFileName, img)
            return newFileName
        case "rmbg":
            newFileName = f'static/{filename}'
            img = cv2.imread(f'{UPLOAD_FOLDER}/{filename}')
            newFileName = remove(img)
            cv2.imwrite(newFileName, img)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == "POST":
        if 'file' not in request.files:
                flash('No file part')
                return 'error'
        file = request.files['file']
            
        if file.filename == '':
                    flash('No selected file')
                    return "error no file selected"
        if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    operation = request.form.get('operation')
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    new = proccessImage(filename=filename, operation=operation)
                    flash(f'Image Converted Successfully. Download it from <a href="/{new}" target="_blank">here</a>')
                    return render_template('index.html')               
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)