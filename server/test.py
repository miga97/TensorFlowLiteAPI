from fastapi import FastAPI
from typing import Optional
import wget
import time
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {"Name": "TensorFlowLiteAPI"}


@app.get("/process")
def read_process(name: str, url: str, token: Optional[str] = None):
    path = './tmp'

    if token is not None: 
      site = url + '?token=' + token
    else:
      site = url
    
    filename = str(int(round(time.time() * 1000)))
    filename = filename + '.jpg'
    wget.download(site, path +'/' + filename)

    #process the image
    #time.sleep(5)

    os.remove(path +'/' + filename)

    return {"url": url, "name": name +' - ' + filename}