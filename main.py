from flask import Flask, render_template, redirect
from forms import UploadFileForm
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "changeMe"
app.config["UPLOAD_FOLDER"] = "static/files"


@app.route("/", methods=["GET", "POST"])
def index():
    form = UploadFileForm()

    if form.validate_on_submit():
        file = form.file.data

        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))

        with open(file="file.txt") as f:
            s = f.read().strip().split(" ")

            tf = {}

            for i in s:
                if i == "":
                    s.pop(s.index(i))
                    continue

                if i in tf:
                    tf[i] += 1
                else:
                    tf[i] = 1

        tf = sorted(tf.items(), key=lambda item: item[1], reverse=True)

        wordsCount = 0
        for el in tf:
            wordsCount += el[1]

        return render_template('result.html', tf=tf, wordsCount=wordsCount)
    return render_template('index.html', form=form)

