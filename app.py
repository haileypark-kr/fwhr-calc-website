# from http.client import PRECONDITION_FAILED
from flask import Flask, request, send_file, redirect
from flask_cors import CORS
# from flask import jsonify, make_response
# from werkzeug.utils import secure_filename
# import pandas as pd
import os
import logging
import argparse

from fWHR_calc import analyze_face
from config import ERROR_DATA_FOLDER, PRETRAINED_MODEL_PATH, UPLOAD_FOLDER, OUTPUT_FOLDER
from utils import clear_directory, make_directory

app = Flask('fwhr')
app.config['LOGGING_LEVEL'] = logging.DEBUG
app.config['LOGGING_FORMAT'] = '%(asctime)s%(levelname)s:%(message)sin %(filename)s:%(lineno)d]'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

CORS(app)


@app.route("/", methods=["GET"])
def index():
    return app.send_static_file('index.html')


@app.route('/uploader', methods=["GET", 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file")

        clear_directory(app.config['UPLOAD_FOLDER'])

        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        saved_file_path, saved_filename = analyze_face(app.config['UPLOAD_FOLDER'], ERROR_DATA_FOLDER,
                                                       PRETRAINED_MODEL_PATH, app.config['OUTPUT_FOLDER'])

        return send_file(saved_file_path,
                         attachment_filename=saved_filename,
                         as_attachment=True)
    return redirect("/")


if __name__ == "__main__":

    # load_dotenv()
    make_directory(ERROR_DATA_FOLDER)
    make_directory(app.config['UPLOAD_FOLDER'])
    clear_directory(app.config['UPLOAD_FOLDER'])
    make_directory(app.config['OUTPUT_FOLDER'])

    app.run(host='127.0.0.1', port=5001, debug=False)
