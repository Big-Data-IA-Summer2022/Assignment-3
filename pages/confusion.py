from google.cloud import bigquery
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =  '/keys/key.json'
def confusionmat():
    client = bigquery.Client()
    max=client.query(f"""SELECT * FROM `defect-detection-356414.for_logs.confusion-matrix`""").to_dataframe()
    df = pd.DataFrame(max)
    confusion_matrix = pd.crosstab(df['actual'], df['predicted'], rownames=['actual'], colnames=['predicted'])
    return confusion_matrix

def app():
    st.title("Binary Classification for defect or ok")
    st.markdown("# Confusion matrix of predictions made using Airflow")

    st.write(
        """print confusion matrix for airflow prediction """
    )
    st.write(confusionmat())
    st.snow()
