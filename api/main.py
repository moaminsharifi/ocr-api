from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from ocr.router import router as ocr_router
from dependencies import get_token_header


app = FastAPI()

app.include_router(
    ocr_router,
    prefix="/ocr",
    tags=["ocr"],
    dependencies=[Depends(get_token_header)],
)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"data": "success"}
