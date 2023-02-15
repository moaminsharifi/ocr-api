import base64
import io
import numpy as np
from PIL import Image
import cv2

from config import get_model, get_processor


def process_image_with_deep_learning_model(image: np.array) -> str:
    """process image with deep learning model

    Args:
        image (np.array): input image to

    Returns:
        str: output result as a string
    """
    image = Image.fromarray(image).convert("RGB")
    processor = get_processor()
    model = get_model()

    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text


def base_64_to_image(base64_string: str) -> np.array:
    """Take in base64 string and return cv image

    Args:
        base64_string (str): base64 string

    Returns:
        np.array: numpy array image
    """
    img_data = base64.b64decode(str(base64_string))
    img = Image.open(io.BytesIO(img_data))
    opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    return opencv_img


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
