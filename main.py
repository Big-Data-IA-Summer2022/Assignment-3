import os
import logging
import pandas as pd
import models
from database import engine, SessionLocal
from dotenv import load_dotenv
from routers import users, authentication
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.staticfiles import StaticFiles
import json
import schemas
from routers.oaut2 import get_current_user
from fastapi import FastAPI,status,HTTPException
##########################################################################

load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('BQ_KEY_JSON')
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=LOGLEVEL,
    datefmt='%Y-%m-%d %H:%M:%S')

###########################################################################

app = FastAPI(title="Main App")

@app.get("/Login here:")
def login(get_current_user: schemas.ServiceAccount = Depends(get_current_user)):
    return {"Hello Python"}

#app.include_router(data.router)
app.include_router(users.router)
app.include_router(authentication.router)
#app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

models.Base.metadata.create_all(bind=engine)