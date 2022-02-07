import os
import shutil
import numpy as np
from config import FACE_API_KEY_CONFIG_FILE, FACE_API_URL
import dlib
import pandas as pd
from imutils import face_utils
from tqdm import tqdm
from datetime import datetime
import logging
import requests
import cv2
from skimage import io
from utils import make_directory, is_allowed_file


def get_fWHR(dataroot, log_path, filepath, detector, predictor):

    # lists that contain file names with error
    load_error_path = log_path + "OpenError/"
    no_face_path = log_path + "NoFace/"
    many_faces_path = log_path + "ManyFaces/"

    full_filepath = os.path.join(dataroot, filepath)

    fWHR = 0
    width = 0
    height = 0
    xy_coordinates = []

    if is_allowed_file(filepath):
        filename = filepath.split('.')[0]

        try:
            image = cv2.imread(full_filepath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        except Exception:
            logging.warn(
                "Warning: opencv was unable to open the image. skimage will be used alternatively.")
            try:
                gray = io.imread(full_filepath, as_gray=True)
            except:
                return width, height, fWHR, []

        data = np.asarray(gray)

        # check whether the image file is an appropriate file
        # if the image is empty, it will be copied to
        # load_error_path folder.
        try:
            _data = data[0][0]
        except Exception:
            shutil.copy(full_filepath, load_error_path + filepath)
            logging.error(
                "Error: image is not appropriate - {}".format(filepath))
            return width, height, fWHR, []

        # detect faces in image
        # if the image has no face detected,
        # it will be copied to
        # load_error_path folder.
        rects = []
        try:
            rects = detector(gray, 1)
            rect = rects[0]

        except Exception as e:
            logging.error(
                "Error: cannot detect face - {} {}".format(filepath, e))
            shutil.copy(full_filepath, no_face_path + filepath)
            return width, height, fWHR, []

        # if multiple faces are detected,
        # copy the image to "ManyFace" directory
        # you have to check these images one by one
        if len(rects) > 1:
            logging.error(
                "Error: multiple face detected - {}".format(filepath))
            shutil.copy(full_filepath, many_faces_path + filepath)
            return width, height, fWHR, []

        elif len(rects) == 1:
            rect = rects[0]
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = predictor(gray, rect)

            shape = face_utils.shape_to_np(shape)

            # landmarks used in calculating fWHR
            fWHR_landmarks = [shape[1], shape[15],
                              shape[21], shape[22], shape[51]]

            # calculate width and height for fWHR
            width = ((fWHR_landmarks[0][0] - fWHR_landmarks[1][0]) ** 2 +
                     (fWHR_landmarks[0][1] - fWHR_landmarks[1][1]) ** 2) ** (0.5)

            avg_21_22 = (fWHR_landmarks[2] + fWHR_landmarks[3]) / 2.0
            height = ((avg_21_22[0] - fWHR_landmarks[4][0]) ** 2 +
                      (avg_21_22[1] - fWHR_landmarks[4][1]) ** 2) ** (0.5)

            fWHR = width / float(height)

            xy_coordinates = np.concatenate(shape)

    return width, height, fWHR, xy_coordinates


def get_face_api_result(face_api_key, image_path):
    image_url = open(image_path, 'rb').read()

    headers = {'Ocp-Apim-Subscription-Key': face_api_key,
               'Content-Type': 'application/octet-stream'}

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur',
    }

    response = requests.post(FACE_API_URL, params=params,
                             headers=headers, data=image_url)

    faces = response.json()
    f = []

    if response.status_code != 200:
        logging.error(
            "Error - FaceApi response status is not OK - {}".format(image_path))

        return [""] * 14

    try:
        features = faces[0]["faceAttributes"]

        f = [features["age"], features['gender'], features["emotion"]["fear"], features["emotion"]["sadness"], features["emotion"]["disgust"],
             features["emotion"]["contempt"], features["emotion"]["neutral"], features["emotion"]["happiness"], features["emotion"]["anger"],
             features["glasses"], features["facialHair"]["moustache"], features["facialHair"]["beard"], features["facialHair"]["sideburns"],
             features["hair"]["bald"]]

    except Exception as e:
        logging.error(
            "Error - cannot analyze image with FaceApi - {}, {}".format(image_path, e))
        pass

    return f


def analyze_face(dataroot, log_path, shape_predictor_path, out_path):
    # initialize face detector and facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor_path)

    make_directory(os.path.join(log_path, "OpenError/"))
    make_directory(os.path.join(log_path, "ManyFaces/"))
    make_directory(os.path.join(log_path, "NoFace/"))

    out = []

    # load Azure Face Api Key file
    try:
        with open(FACE_API_KEY_CONFIG_FILE, "r") as f:
            FACE_API_SUBSCRIPTION_KEY = f.readline()
    except Exception as execptionOpeningKeyfile:
        logging.error(
            "Error - Cannot open Face API key conf file - {}".format(FACE_API_KEY_CONFIG_FILE))

    # loop over every image in dataroot
    for filepath in tqdm(os.listdir(dataroot)):
        # fwhr result
        width, height, fWHR, xy_coordinates = get_fWHR(
            dataroot, log_path, filepath, detector, predictor)
        if fWHR != 0 and len(xy_coordinates) == 136:
            row = [filepath.split('.')[0], width, height, fWHR]
            row.extend(xy_coordinates)
        else:
            row = [filepath.split('.')[0]]
            row.extend([0] * 139)

        # face api result
        full_filepath = os.path.join(dataroot, filepath)
        faceapi_result = get_face_api_result(
            FACE_API_SUBSCRIPTION_KEY, full_filepath)
        row.extend(faceapi_result)

        # merge two results
        out.append(row)

    columns = ['FileName', 'Width', 'Height', 'fWHR']
    for i in range(68):
        columns.append("x{}".format(i+1))
        columns.append("y{}".format(i+1))
    columns.extend(["Age", "Gender", "Fear", "Sadness", "Disgust", "Contempt", "Neutral", "Happiness", "Anger", "Glasses", "Moustache", "Beard", "Sideburns",
                    "Bald"])

    outf = pd.DataFrame(out, columns=columns)

    timestamp = datetime.today().strftime('%Y%m%d_%H%M%S')
    filename = "fWHR_{}.xlsx".format(timestamp)
    filepath = os.path.join(out_path, filename)
    outf.to_excel(filepath, index=False)
    return filepath, filename
