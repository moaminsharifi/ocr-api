from pydantic import BaseSettings
from functools import lru_cache
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


class Settings(BaseSettings):
    app_name: str = "API"
    app_env: str = "localhost"
    api_token: str = "2d994837-ec32-4250-8a7c3e85babf096"

    class Config:
        env_file = ".env"


@lru_cache()
def get_model():
    return VisionEncoderDecoderModel.from_pretrained("/app/trocr-small-printed")


@lru_cache()
def get_processor():
    return TrOCRProcessor.from_pretrained("/app/trocr-small-printed")


@lru_cache()
def get_settings():
    return Settings()
