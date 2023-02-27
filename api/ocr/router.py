from fastapi import APIRouter
from ocr.request_models import ProcessOcrRequest
from ocr.utils import (
    pre_process_captcha_image,
    base_64_to_image,
    process_image_with_deep_learning_model,
)

router = APIRouter()


@router.post("")
async def process(request: ProcessOcrRequest):
    try:
        image = base_64_to_image(request.image)
    except:
        raise ValueError("Invalid image: %s" % request.image)


    result = process_image_with_deep_learning_model(image)
    return {"data": result}
