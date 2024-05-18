# -*- coding: utf-8 -*-
from parser import parsing
from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
async def root():
    path_list = ["/Users/tanya/Desktop/hack_heart/test_dir/dir_2", "/Users/tanya/Desktop/hack_heart/test_dir/dir_1"]
    return parsing(path_list)
