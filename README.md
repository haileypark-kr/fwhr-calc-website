# fwhr-calc-website
This project is to automatically measure the facial Width-To-Height Ratio and get facial analysis results provided by Microsoft Azure Cognitive Services.
Used in 
- [The face of risk: CEO facial masculinity and firm risk](https://onlinelibrary.wiley.com/doi/10.1111/eufm.12175) by Shinichi Kamiya, Y. Han (Andy) Kim, Soohyun Park (Me)
- "부자, 관상, 기술" written by Y. Han (Andy) Kim

# What you can get 
You can get some estimatations of below (per image):
- Facial Width-To-Height Ratio
- X, y coordinates for 68 facial landmarks

- If you use Microsoft Face APIs:
    - Age
    - Gender
    - Emotions
        - fear, sadness, disgust, contempt, neutral, happiness, anger 
    - Glasses / no glasses
    - Moustache
    - Beard
    - Sideburns
    - Bald


# Notice about usage of Microsoft Face API
Since June 11th, 2020, Microsoft Azure Face recognition services are strictly prohibited for use by or for US police departments. Read [this announcement](https://learn.microsoft.com/en-us/legal/cognitive-services/computer-vision/limited-access-identity?context=%2Fazure%2Fcognitive-services%2Fcomputer-vision%2Fcontext%2Fcontext
)


# Built with
- Python 3.6
- Dlib
- Opencv
- Flask


# Getting started

## Prerequisites
1. python version **3.6** with **Anaconda distribution** (no guarantee for other versions)
    - You can download Anaconda Individual Edition in [here](https://www.anaconda.com/products/individual)
    - Check your anaconda installation by `conda -V`
    - Create a virtual environment by `conda create -n [name] python=3.6` and activate the venv by `conda activate [name]`
2. Clone this repo
    - `git clone https://github.com/haileypark-kr/fwhr-calc-website.git`
    - Move to the project root directory. `cd fwhr-calc-website`
3. Microsoft Azure Face Api Key
    1. Create an Azure account and a Cognitive Service Face API resource in Azure Portal. Read [this](https://docs.microsoft.com/en-us/azure/cognitive-services/face/) documentation.
    2. Generate keys to access your API. (Resource Management > Keys and Endpoint)
    3. Make a file named `azure_faceapi_key.conf` and paste the first key in the file. (you can change the file name if you want, but make sure you also change `.gitignore `and `config.py`) Do not upload this file to GitHub.
    4. Replace the variable `FACE_API_ENDPOINT` in `config.py` with your endpoint.
        ```
        # config.py
        
        FACE_API_ENDPOINT = "https://eastasia.api.cognitive.microsoft.com"
        ```


# Installation

Install python libraries in this project's root directory.
1. `pip install -r requirements.txt`
2. `conda install -y -c conda-forge dlib`
    - Some libraries (e.g. dlib) cannot be installed by pip - should be installed using `conda`.

# Usage

There are two ways to run this application.
- Running a flask web server: If you want to analyze a few facial images with GUI. 
- Running fWHR calcaculating script: If you want to analyze thousands of images. 

### Running a flask web server
1. Command: `python app.py`
2. Open a Chrome browser and enter `127.0.0.1:5001`
3. Select some images and press Submit button.
4. Wait and **do not reload the browser**.
5. Anlysis result will be downloaded shortly. (in xlsx format)


### Running fWHR calcaculating script
1. Command: `python fWHR_main.py --dataroot [path to the image directory]`
2. Wait
3. Go to `data/output` direcetory and get the analysis result file.



# Configurations

You can change configuration values configured in `config.py`.

1. directory path configs 
    - UPLOAD_FOLDER: directory to save uploaded images via flask web server
    - OUTPUT_FOLDER: directory to save output images
    - ERROR_DATA_FOLDER: directory to save images where this application couldn't find any faces
    - PRETRAINED_MODEL_PATH: path to pretrained model. Either a relative path from this project root directory or an absolute path.

2.  image configs
    - ALLOWED_EXTENSIONS: set of allowed image extensions. case insensitive.

3. Microsoft Azure configs
    - USE_MS_FACE_API: boolean value whether to use Microsoft Face API or not. (False / True)
    - FACE_API_KEY_CONFIG_FILE: name of the config file storing Microsoft Face API key.  You can get this value in Azure portal.
    - FACE_API_ENDPOINT: endpoint of Microsoft Face API. You can get this value in Azure portal.
    - FACE_API_URL: full url for Microsoft Face API. Do not edit this value unless the API's url path is changed.
