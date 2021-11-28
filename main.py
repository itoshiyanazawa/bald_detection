import streamlit as st
from PIL import Image

import requests
from PIL import ImageDraw
import io

st.title('顔認識アプリ')

KEY = "5f47d596a70445c599391658743da07d"
assert KEY

face_api_url = 'https://20211128.cognitiveservices.azure.com/' + '/face/v1.0/detect'


uploaded_file = st.file_uploader('Choose an image...', type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output, format='JPEG')
        binary_img = output.getvalue()

    headers = {
        'Content-Type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key': KEY
        }

    params = {
        'returnFaceAttributes': 'age,gender,smile,facialHair,headPose,glasses',
        'returnFaceId': 'true'
    }

    response = requests.post(face_api_url, params=params,
    headers=headers, data=binary_img
    )

    results = response.json()

    for result in results:
        result = result['faceRectangle']

        draw = ImageDraw.Draw(img)
        draw.rectangle([(result['left'],result['top']),(result['left']+result['width'],result['top']+result['height'])],
        fill=None, outline='green',width=5)

    st.image(img, caption='Uploaded Image.', use_column_width=True)

