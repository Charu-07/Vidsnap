from flask import Flask, render_template, request,flash,redirect,url_for
import uuid
import os
from werkzeug.utils import secure_filename
import subprocess
import sys

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods = ["GET", "POST"])
def create():
    if request.method == "GET":
        my_id = uuid.uuid1()
        return render_template("create.html", my_id=my_id)
    
    my_id = uuid.uuid1()
    rec_id = request.form.get("uuid") #for every user a unique id is created
    user_text = request.form.get("text")
    input_files=[]
    for key,value in request.files.items():
        file = request.files[key]

        if file:
            filename = secure_filename(file.filename)
            os.makedirs((os.path.join(app.config['UPLOAD_FOLDER'],rec_id)),exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],rec_id, filename))
            input_files.append(filename)
        with open(os.path.join(app.config['UPLOAD_FOLDER'],rec_id, "user_text.txt"),"w") as f:
            f.write(user_text)
        
    with open(os.path.join(app.config['UPLOAD_FOLDER'],rec_id, "input.txt"),"w") as fl:
        for index,f in enumerate(input_files):
            dur = request.form.get(f"duration{index+1}")
            f = f.replace(" ", "_")
            fl.write(f"file '{f}'\nduration {dur}\n")
    subprocess.Popen([sys.executable, "generate_video.py"])
    return render_template("create.html",my_id=my_id)

@app.route("/gallery")
def gallery():
    reels = os.listdir('static/reels')
    print(reels)
    return render_template("gallery.html",reels = reels)

app.run(debug=True)