# -*- coding: utf-8 -*-
from parser import parsing
from fastapi import FastAPI

from settings import Settings

settings = Settings()

app = FastAPI()


@app.get("/")
async def root():
    path_list = settings.path
    return parsing(path_list)
