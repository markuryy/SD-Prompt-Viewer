from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import json
import os
import base64

app = Flask(__name__)

# Configure the app
app.secret_key = 'hcfwauohczhmocwzhozcmwzoh'
app.config["TEMPLATES_AUTO_RELOAD"] = True
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_data(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def extract_metadata(image_path):
    with Image.open(image_path) as img:
        metadata = img.info
        return {k: (v.decode('utf-8') if isinstance(v, bytes) else v) for k, v in metadata.items()}

@app.route("/", methods=["GET", "POST"])
def home():
    metadata = None
    image_data = None
    filename = ""
    if request.method == "POST":
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(temp_path)

            metadata = extract_metadata(temp_path)
            image_data = get_image_data(temp_path)

    return render_template("index.html", metadata=metadata, image_data=image_data, filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
