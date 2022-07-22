import requests
import json
import os
import sys
from PIL import Image
import os, os.path
import io
from google.cloud import bigquery

imgsdef = []
pathdef = r"C:\Users\abhij\Downloads\archive\casting_data\casting_data\test\def_front"
for f in os.listdir(pathdef):
    imgsdef.append(Image.open(os.path.join(pathdef,f)))
imgsok = []
pathok = r"C:\Users\abhij\Downloads\archive\casting_data\casting_data\test\ok_front"
for f in os.listdir(pathok):
    imgsok.append(Image.open(os.path.join(pathok,f)))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =  os.path.join(sys.path[0], "key.json")


def populatetable(actual: str, predicted: str):
    client = bigquery.Client()
    rows_to_insert =[{"actual":actual, "predicted":predicted}]
    errors = client.insert_rows_json('defect-detection-356414.for_logs.confusion-matrix', rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))



url = "https://damg7245-assignment03-api-xd232aklcq-uc.a.run.app/login"
urlp = 'https://damg7245-assignment03-api-xd232aklcq-uc.a.run.app/predict_with_augmented_data_trained_model'

payload={'username': 'kunjiraman.a@northeastern.edu', 'password': 'ucbp2QYV4bs'}
response = requests.request("POST", url, data=payload)
if response.status_code == 200:
    json_data = json.loads(response.text)
    print('login successful')
    print(json_data["access_token"])




def validate():
    for i in os.listdir(pathok):
        i=os.path.join(pathok,i)
        im = Image.open(i)
        im_resize = im.resize((300, 300))
        buf = io.BytesIO()
        im_resize.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        headers = {}
        headers['Authorization'] = "Bearer " + json_data["access_token"]
        response = requests.request("POST", url=urlp, files={'file': byte_im}, headers=headers)
        text=response.text
        print(text)
        if response.status_code == 200:
            if text == '"defect"':
                text='defect'
            elif text=='"ok"':
                text='ok'
        actual='ok'
        predicted=text
        populatetable(actual, predicted)
    for i in os.listdir(pathdef):
        i=os.path.join(pathdef,i)
        im = Image.open(i)
        im_resize = im.resize((300, 300))
        buf = io.BytesIO()
        im_resize.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        headers = {}
        headers['Authorization'] = "Bearer " + json_data["access_token"]
        response = requests.request("POST", url=urlp, files={'file': byte_im}, headers=headers)
        text=response.text
        print(text)
        if response.status_code == 200:
            if text == '"defect"':
                text='defect'
            elif text=='"ok"':
                text='ok'
        actual='defect'
        predicted=text
        populatetable(actual, predicted)
validate()


