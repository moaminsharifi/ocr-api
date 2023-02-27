from fastapi import APIRouter
from ocr.request_models import ProcessOcrRequest
import uuid
import tempfile
import os
from ocr.utils import (
    pre_process_captcha_image,
    base_64_to_image,
    process_image_with_deep_learning_model,
)

router = APIRouter()


@router.post("")
async def process(request: ProcessOcrRequest):
    temp_dir = tempfile.mkdtemp()
    file_name = f"{temp_dir}/{uuid.uuid4()}.png"
    try:
        image_data = base_64_to_image(request.image)
       

    except:
        raise ValueError("Invalid image: %s" % request.image)
    
    with open(file_name, "wb") as f:
          f.write(image_data)
    result = process_image_with_deep_learning_model(file_name)
    
    if os.path.exists(file_name):
        os.remove(file_name)

    return {"data": result}
