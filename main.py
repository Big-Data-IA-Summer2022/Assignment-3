import os
import logging
import pandas as pd
import models
from database import engine, SessionLocal
from dotenv import load_dotenv
from routers import users, authentication
from fastapi import FastAPI, Depends, status, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
import json
import schemas
from routers.oaut2 import get_current_user
from fastapi import FastAPI,status,HTTPException
from typing import Union
import uvicorn
from keras.models import load_model
from PIL import Image
import numpy as np
from skimage import transform
from io import BytesIO
from starlette.responses import RedirectResponse
import sys
from logfunc import logfunc
##########################################################################

load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =  os.path.join(sys.path[0], "key.json")
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=LOGLEVEL,
    datefmt='%Y-%m-%d %H:%M:%S')

###########################################################################

app_desc = """<h2>Try this app by uploading any image with `predict/image`</h2>
<h2>Defect and non defect checker for manufacture parts api</h2>"""


app = FastAPI(title='Abhi', description=app_desc)

def read_imagefile(file) -> Image.Image:
    try:
        image = Image.open(BytesIO(file))
    except Exception as e:
        logging.error(f"Unable to read the image file, Please check if the image file ends with jpeg,jpg or png")
        return 100
    return image
    

app.include_router(authentication.router)


models.Base.metadata.create_all(bind=engine)

@app.post("/predict_with_augmented_data_trained_model")
async def predict(file: UploadFile = File(...),get_current_user: schemas.ServiceAccount = Depends(get_current_user)):
    image = read_imagefile(await file.read())
    try:
        np_image = np.array(image).astype('float32')/255
        np_image = transform.resize(np_image, (300, 300, 1))
        np_image = np.expand_dims(np_image, axis=0)
    except Exception as e:
        logging.error(f"Numpy unable to process the image")
        return 100
    image = np_image
    try:
        aughdf5=os.path.join(sys.path[0], "cnn_casting_inspection_model.hdf5")
        model= load_model(aughdf5)
    except Exception as e:
        logging.error(f"Unable to read the model")
        return 100
    try:
        ypred= model.predict(image)
    except Exception as e:
        logging.error(f"Model not able to make prediction on given image")
        return 100
    if ypred<0.5:
        result='ok'
    else:
        result='defect'
    return result

@app.post("/predict_with_non_augmented_data_trained_model")
async def predict(file: UploadFile = File(...),get_current_user: schemas.ServiceAccount = Depends(get_current_user)):
    image = read_imagefile(await file.read())
    try:
        np_image = np.array(image).astype('float32')/255
        np_image = transform.resize(np_image, (300, 300, 1))
        np_image = np.expand_dims(np_image, axis=0)
    except Exception as e:
        logging.error(f"Numpy unable to process the image")
        return 100
    image = np_image
    try:
        nonaughdf5=os.path.join(sys.path[0], "cnn_casting_inspection_modelnonaug.hdf5")
        model= load_model(nonaughdf5)
    except Exception as e:
        logging.error(f"Unable to read the model")
        return 100
    try:
        ypred= model.predict(image)
    except Exception as e:
        logging.error(f"Model not able to make prediction on given image")
        return 100
    print(ypred)
    if ypred>0.5:
        result='ok'
    else:
        result='defect'
    return result


@app.get("/")
async def index():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
