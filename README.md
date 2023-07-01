# fwhr-calc-website
This project is to automatically calculate the facial Widht-To-Height ratio and get facial analysis results provided by Microsoft Azure.


# Built with
- Python 3.6
- Dlib
- Opencv
- Flask


# Getting started

## Prerequisites
1. python version **3.6** with **Anaconda distribution** (no guarantee for other versions)
    - You can download Anaconda Individual Edition in [here] (https://www.anaconda.com/products/individual)
    - Check your anaconda installation by `conda -V`
    - Create a virtual environment by `conda create -n [name] python=3.6` and activate the venv by `conda activate [name]`
2. Clone this repo.
    - `git clone https://github.com/haileypark-kr/fwhr-calc-website.git`
3. Microsoft Azure Face Api Key
    1. Create an Azure account and a Cognitive Service Face API resource in Azure Portal. Read [this] (https://docs.microsoft.com/en-us/azure/cognitive-services/face/) documentation.
    2. Generate keys to access your API. (Resource Management > Keys and Endpoint)
    3. Make a file named `azure_faceapi_key.conf` and paste the first key in the file. (you can change the file name if you want, but make sure you also change `.gitignore `and `config.py`) Do not upload this file to GitHub.
    4. Replace the variable `FACE_API_ENDPOINT` in `config.py` with your endpoint.
        ```
        # config.py
        
        FACE_API_ENDPOINT = "https://eastasia.api.cognitive.microsoft.com"
        ```


# Installation
Install python libraries in this project's root directory.
    - `pip install -r requirements.txt`
    - Some libraries (dlib) cannot be installed by pip - should be installed using conda with `conda install -y -c conda-forge dlib`

# Usage
There are two ways to run this application.
    - Running a flask web server: If you want to analyze a few facial images with GUI.
    - Running fWHR calcaculating script: If you want to analyze thousands of images

## Running a flask web server
1. Command: `python app.py`
2. Open a Chrome browser and enter `127.0.0.1:5001`
3. Select some images and press Submit button.
4. Wait and do not reload the browser.
5. Anlysis result will be downloaded shortly (in xlsx format)


## Running fWHR calcaculating script
1. Command: `python fWHR_main.py --dataroot [path to the image directory]`
2. Wait
3. Go to `data/output` direcetory and get the analysis result file.


# Configurations

You can change config values configured in `config.py`.

1. directory path configs 
    - UPLOAD_FOLDER: directory to save uploaded images via flask web server
    - OUTPUT_FOLDER: directory to save output images
    - ERROR_DATA_FOLDER: directory to save images where this application couldn't find any faces
    - PRETRAINED_MODEL_PATH: path to pretrained model. Either a relative path from this project root directory or an absolute path.

2.  image configs
    - ALLOWED_EXTENSIONS: set of allowed image extensions. case insensitive.

3. Microsoft Azure configs
    - FACE_API_KEY_CONFIG_FILE: name of the config file storing Microsoft Face API key.  You can get this value in Azure portal.
    - FACE_API_ENDPOINT: endpoint of Microsoft Face API. You can get this value in Azure portal.
    - FACE_API_URL: full url for Microsoft Face API. Do not edit this value unless the API's url path is changed.
    - FACE_API_SLEEP_TIME: sleep seconds(not milliseconds) between Microsoft Face API calls. Set 3 if you are using a Free0 tier pricing. If you are using Standard0 pricing, set this value 0. 