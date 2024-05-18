# -*- coding: utf-8 -*-
from parser import parsing
from fastapi import FastAPI
from dotenv import load_dotenv, dotenv_values
import os

app = FastAPI()

@app.get("/")
async def root():
    load_dotenv()
    print(os.getenv("DIR_PATH"))
    return parsing([os.getenv("DIR_PATH")])
