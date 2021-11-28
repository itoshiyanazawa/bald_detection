import streamlit as st
from PIL import Image
from PIL import ImageFont
import requests
from PIL import ImageDraw
import io

st.title('ハゲ度Check!')

st.subheader('ハゲ度の目安')
st.write('0~25%:　:smile:, 25~30%: :worried:, 31~100%: :innocent:')


KEY = "5f47d596a70445c599391658743da07d"
assert KEY

face_api_url = 'https://20211128.cognitiveservices.azure.com/' + '/face/v1.0/detect'


uploaded_file = st.file_uploader('JPG形式の画像を選択してください', type='jpg')
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
        'returnFaceAttributes': 'age,gender,smile,facialHair,headPose,glasses,Hair',
        'returnFaceId': 'true'
    }

    response = requests.post(face_api_url, params=params,
    headers=headers, data=binary_img
    )

    results = response.json()

    for result in results:
        bald = result['faceAttributes']['hair']['bald']
        result = result['faceRectangle']

        if bald >= 0.31:
            st.write('Result: :innocent:')
        
        elif bald >= 0.25:
            st.write('Result: :worried:') 

        else:
            st.write('Result: :smile:')
        
       

        draw = ImageDraw.Draw(img)
        draw.rectangle([(result['left'],result['top']),(result['left']+result['width'],result['top']+result['height'])],
        fill=None, outline='green',width=5)
        font = ImageFont.truetype("40231058178.ttf",50)
        draw.text((result['left'],result['top']-60),'ハゲ度: {}%'.format(bald),(255,0,255),font=font)

    st.image(img, caption='Uploaded Image.', use_column_width=True)
    st.write('※判断基準はあくまで目安です。誤認識する場合があります。')



