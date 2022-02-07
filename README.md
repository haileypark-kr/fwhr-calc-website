# fwhr-calc-website
This project is to automatically measure the facial Width-To-Height ratio and get facial analysis results provided by Microsoft Azure.
Used in 
- [The face of risk: CEO facial masculinity and firm risk] (https://onlinelibrary.wiley.com/doi/10.1111/eufm.12175) by Shinichi Kamiya, Y. Han (Andy) Kim, Soohyun Park (Me)
- "부자, 관상, 기술" written by Y. Han (Andy) Kim

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
