from google.cloud import bigquery
from dotenv import load_dotenv
import os

#################################################
# Author: Abhijit
# Creation Date: 17-Jun-22
# Last Modified Date:
# Change Logs:
# SL No         Date            Changes
# 1             17-Jun-22       First Version
# 2             24-Jun-22       Log Function
#################################################

def logfunc(endpoint:str, response_code: int):
    load_dotenv()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('BQ_KEY_JSON')
    client = bigquery.Client()
    max=client.query(f"select max(logid)+1, string(current_timestamp()) as tstamp from `plane-detection-352701.SPY_PLANE.logs`").result()
    for i in max:
        var= i[0]
        tstamp=i[1]
    print(var)
    rows_to_insert =[{"logtime":tstamp, "endpoint": endpoint, "response_code": response_code,"logid":var}]
    errors = client.insert_rows_json('plane-detection-352701.SPY_PLANE.logs', rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))
