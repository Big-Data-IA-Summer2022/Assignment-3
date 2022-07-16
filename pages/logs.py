import streamlit as st
from google.cloud import bigquery
import os
import sys
import pandas as pd
from dotenv import load_dotenv



load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =  '/keys/key.json'
def queries():
    client = bigquery.Client()
    df = client.query(f"""SELECT * FROM `defect-detection-356414.for_logs.logs` order by logid desc""").to_dataframe()
    return df
def app():
    st.markdown("# logs")
    st.write('The following are the records')
    df=pd.DataFrame(queries())
    st.dataframe(df)
    chart=df['endpoint'].value_counts()
    st.markdown('Bar chart displaying counts of all endpoints:')
    st.bar_chart(chart)
