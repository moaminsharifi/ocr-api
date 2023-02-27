import base64
import io
import numpy as np
from PIL import Image
import cv2

from config import get_model
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

img_width = 200
img_height = 50


def encode_single_sample(img_path):
    # 1. Read image
    img = tf.io.read_file(img_path)
    # 2. Decode and convert to grayscale
    img = tf.io.decode_png(img, channels=1)
    # 3. Convert to float32 in [0, 1] range
    img = tf.image.convert_image_dtype(img, tf.float32)
    # 4. Resize to the desired size
    img = tf.image.resize(img, [img_height, img_width])
    # 5. Transpose the image because we want the time
    # dimension to correspond to the width of the image.
    img = tf.transpose(img, perm=[1, 0, 2])
    # 6. Return a dict as our model is expecting two inputs
    return tf.reshape(img, [1, img_width, img_height, 1])


def decode_batch_predictions(pred, max_length=5):
    characters = sorted(list(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]))

    # Mapping characters to integers
    char_to_num = layers.StringLookup(vocabulary=list(characters), mask_token=None)

    # Mapping integers back to original characters
    num_to_char = layers.StringLookup(
        vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True
    )

    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
        :, :max_length
    ]
    # Iterate over the results and get back the text
    output_text = []
    for res in results:
        res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output_text.append(res)
    return output_text


def process_image_with_deep_learning_model(image_path) -> str:
    """process image with deep learning model

    Args:
        image (str): input image path

    Returns:
        str: output result as a string
    """

    img = encode_single_sample(image_path)

    prediction_model = get_model()

    preds = prediction_model.predict(img)
    pred_texts = decode_batch_predictions(preds)
    return pred_texts[0]


def base_64_to_image(base64_string: str):
    """Take in base64 string and return cv image

    Args:
        base64_string (str): base64 string

    Returns:
        np.array: numpy array image
    """
    img_data = base64.b64decode(str(base64_string))
    return img_data


def pre_process_captcha_image(img_data: np.array) -> np.array:
    """preProcess captcha image using opencv

    Args:
        img_data (np.array): input image

    Returns:
        np.array: output image
    """
    # convert to grayscale
    gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)

    # blur
    blur = cv2.GaussianBlur(gray, (0, 0), sigmaX=33, sigmaY=33)

    # divide
    divide = cv2.divide(gray, blur, scale=255)

    # otsu threshold
    thresh = cv2.threshold(divide, 0, 255, cv2.THRESH_BINARY_INV)[1]

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closing = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

    return np.array(closing)
