from pydantic import BaseSettings
from functools import lru_cache
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np


class Settings(BaseSettings):
    app_name: str = "API"
    app_env: str = "localhost"
    api_token: str = "2d994837-ec32-4250-8a7c3e85babf096"

    class Config:
        env_file = ".env"


@lru_cache()
def get_model():
    model = tf.keras.models.load_model('ocr-model')

    return keras.models.Model(
        model.get_layer(name="image").input, model.get_layer(name="dense2").output
    )


@lru_cache()
def get_processor():
    return TrOCRProcessor.from_pretrained("/app/trocr-small-printed")


@lru_cache()
def get_settings():
    return Settings()
