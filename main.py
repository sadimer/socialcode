# -*- coding: utf-8 -*-
import os
from http.client import HTTPException

from parser import parsing
from fastapi import FastAPI, UploadFile

from settings import Settings

settings = Settings()

app = FastAPI()


@app.get("/")
async def root():
    path_list = settings.path_dir.split(",")
    new_list = []
    for path in path_list:
        if path:
            new_list.append(path)
    if not os.path.exists(settings.tmp_dir):
        os.makedirs(settings.tmp_dir)
    new_list.append(settings.tmp_dir)
    return parsing(new_list)


@app.post(
    "/upload_payment",
    operation_id="upload_payment",
)
async def upload_payment(file: UploadFile):
    contents = await file.read()
    with open(os.path.join(settings.tmp_dir, file.filename), "wb") as new:
        new.write(contents)
