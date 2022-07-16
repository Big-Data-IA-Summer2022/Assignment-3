import streamlit as st
import requests
import json
from PIL import Image
import tempfile
from pathlib import Path

def app():
    st.markdown("# Image based prediction to check whether part is defective or OK")
    st.sidebar.header("augmented model")

    image1='https://pythonmachinelearning.pro/wp-content/uploads/2017/10/DenseNet.png.webp'
    st.image(image1, caption=' Convolutional Neural Network')

    st.write(
        """A Convolutional Neural Network model has been used for predicting """
    )

    image ='https://user-images.githubusercontent.com/20265851/136126372-f8bc20a9-e358-40f8-9d07-4e22e723039f.png'

    st.image(image, caption=' casting manufacturing product defects')


    st.write(
        """The model trained using augmented dataset """
    )

    st.subheader("**We will test the models here :hammer_and_wrench::gear::** ")
    st.markdown('Check if the part in the image is OK or defective.')


    uploaded_file = st.file_uploader("Choose a file")
    buttonstat=st.button('Get Results', disabled=False)
    if buttonstat:

        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                fp = Path(tmp_file.name)
                fp.write_bytes(uploaded_file.getvalue())
                files = {'file': open(tmp_file.name, 'rb')}
                url = 'https://damg7245-assignment03-api-xd232aklcq-uc.a.run.app/predict_with_non_augmented_data_trained_model'
                headers = {}
                headers['Authorization'] = f"Bearer {st.session_state['access_token']}"
                
                response = requests.request("POST", url,files=files, headers=headers)
                text=response.text
                if response.status_code == 200:
                    if text == '"defect"':
                        st.write("The part is defective")
                        notokpic='https://friendlystock.com/wp-content/uploads/2019/08/7-sad-employee-cartoon-clipart.jpg'
                        st.image(notokpic)
                    elif text=='"ok"':
                        st.write("The part is good")
                        okpic="https://static0.gamerantimages.com/wordpress/wp-content/uploads/Vault-Boy-Thumbs-Up.jpg?q=50&fit=contain&w=960&h=500&dpr=1.5"
                        st.image(okpic)
                else:
                    st.error("Error")
