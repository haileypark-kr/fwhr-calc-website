# directory path configs
UPLOAD_FOLDER= "data/uploadedimages/"
OUTPUT_FOLDER = "data/output/"
ERROR_DATA_FOLDER = "data/errors/"
PRETRAINED_MODEL_PATH = "shape_predictor_68_face_landmarks.dat"

# image configs
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Microsoft Azure configs
FACE_API_KEY_CONFIG_FILE = "azure_faceapi_key.conf"
FACE_API_ENDPOINT = "https://eastasia.api.cognitive.microsoft.com"
FACE_API_URL = FACE_API_ENDPOINT + "/face/v1.0/detect"
