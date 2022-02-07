# Soohyun Park and Andy Kim co-developed
# We modified Adrian Rosebrock's python codes in "Facial landmarks with dlib, OpenCV, and Python"
# into an automate fWHR calculator
# This code recognizes 68 facial landmarks, calculates fWHR and saves the results in a csv file
# You can get a xlsx file containing a face width, height and fWHR of each image
#
# USAGE: python fWHR_main.py --dataroot [path_to_images] --face_api_key [key]
#

import logging
from config import ERROR_DATA_FOLDER, OUTPUT_FOLDER, PRETRAINED_MODEL_PATH
from fWHR_calc import analyze_face
import argparse

from utils import clear_directory, make_directory


def main(config):
    make_directory(ERROR_DATA_FOLDER)
    make_directory(OUTPUT_FOLDER)
    analyze_face(config.dataroot, config.log_path,
                 config.predictor_path, config.outf_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataroot', required=True, help="path to the images")
    parser.add_argument('--predictor_path', default=PRETRAINED_MODEL_PATH,
                        help='path to pretrained facial landmark file')
    parser.add_argument('--log_path', default=ERROR_DATA_FOLDER,
                        help='path to save log')
    parser.add_argument('--outf_path', default=OUTPUT_FOLDER,
                        help='path to save result csv files')

    config = parser.parse_args()
    logging.debug("Config:", config)

    main(config)
