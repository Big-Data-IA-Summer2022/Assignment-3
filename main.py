import os
from typing import Union
import uvicorn
import logging
import pandas as pd
from fastapi import FastAPI, File, UploadFile
from keras.models import Sequential, load_model
from PIL import Image
import numpy as np
from skimage import transform
from pydantic import BaseModel
import tensorflow as ts
from io import BytesIO
from starlette.responses import RedirectResponse
import sys


app_desc = """<h2>Try this app by uploading any image with `predict/image`</h2>
<h2>Defect and non defect checker for manufacture parts api - it is just a learning app demo</h2>"""

app = FastAPI(title='Abhi', description=app_desc)

def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image

@app.post("/predict_with_augmented_data_trained_model")
async def predict(file: UploadFile = File(...)):
    image = read_imagefile(await file.read())
    np_image = np.array(image).astype('float32')/255
    np_image = transform.resize(np_image, (300, 300, 1))
    np_image = np.expand_dims(np_image, axis=0)
    image = np_image
    aughdf5=os.path.join(sys.path[0], "cnn_casting_inspection_model.hdf5")
    model= load_model(aughdf5)
    ypred= model.predict(image)
    if ypred<0.5:
        result='ok'
    else:
        result='defect'
    return {result}


@app.post("/predict_with_non_augmented_data_trained_model")
async def predict(file: UploadFile = File(...)):
    image = read_imagefile(await file.read())
    np_image = np.array(image).astype('float32')/255
    np_image = transform.resize(np_image, (300, 300, 1))
    np_image = np.expand_dims(np_image, axis=0)
    image = np_image
    nonaughdf5=os.path.join(sys.path[0], "cnn_casting_inspection_modelnonaug.hdf5")
    model= load_model(nonaughdf5)
    ypred= model.predict(image)
    print(ypred)
    if ypred>0.5:
        result='ok'
    else:
        result='defect'
    return {result}


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, debug=True)